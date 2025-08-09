import streamlit as st
import os
import pandas as pd
import io
from datetime import datetime
from dotenv import load_dotenv

# 로컬 모듈 import
from data_manager import DataFrameManager, process_data_request
from file_processor import process_uploaded_file
from ai_handler import AIHandler, get_model_templates

load_dotenv()
API_KEY = os.environ.get('OPENAI_APIKEY')

# AI 핸들러 초기화
try:
    ai_handler = AIHandler(API_KEY)
except ValueError as e:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경변수 OPENAI_APIKEY를 설정해주세요.")
    st.stop()

# 채팅 기록을 저장할 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}

if "current_df" not in st.session_state:
    st.session_state.current_df = None

if "df_managers" not in st.session_state:
    st.session_state.df_managers = {}

def main():
    st.set_page_config(
        page_title="인공지능 모델링 검증 챗봇",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("🤖 인공지능 모델링 검증 챗봇")
    st.markdown("---")
    
    # 안내 메시지
    with st.container():
        st.markdown("""
        ### 👋 환영합니다!
        
        이 AI 챗봇은 다음과 같은 기능을 제공합니다:
        - 💬 **자연어 대화**: 궁금한 것을 자유롭게 물어보세요
        - 📄 **파일 분석**: 텍스트, CSV, Excel(XLSX), 이미지 파일을 업로드하여 분석을 요청할 수 있습니다
        - 🎛️ **설정 조절**: 사이드바에서 AI의 창의성을 조절할 수 있습니다
        
        시작하려면 아래 버튼을 클릭하거나 메시지를 입력해주세요!
        """)
    
    # 서비스 버튼들
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 정보 검색", use_container_width=True):
            st.session_state.messages.append({
                "role": "user", 
                "content": "최신 정보나 특정 주제에 대해 알고 싶은 것이 있으면 질문해주세요."
            })
            st.rerun()

    with col2:
        if st.button("📊 데이터 분석", use_container_width=True):
            if st.session_state.df_managers:
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "업로드된 데이터로 할 수 있는 작업들을 알려주세요."
                })
            else:
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "데이터 분석이나 해석에 도움이 필요하시면 CSV 또는 Excel(XLSX) 파일을 업로드해주세요."
                })
            st.rerun()
    
    st.markdown("---")
    
    # 데이터 편집기 섹션
    if st.session_state.current_df is not None:
        st.subheader("📊 데이터 편집기")
        
        # DataFrame 선택 옵션 (여러 파일이 업로드된 경우)
        if len(st.session_state.dataframes) > 1:
            selected_file = st.selectbox(
                "편집할 데이터 파일 선택:",
                options=list(st.session_state.dataframes.keys()),
                key="df_selector"
            )
            if selected_file:
                st.session_state.current_df = st.session_state.dataframes[selected_file]
        
        # 데이터 편집기 표시
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**📝 아래에서 데이터를 직접 편집할 수 있습니다:**")
        
        with col2:
            if st.button("💾 변경사항 저장", key="save_changes"):
                st.success("✅ 변경사항이 저장되었습니다!")
                st.rerun()
        
        # 실시간 편집 가능한 데이터 테이블
        edited_df = st.data_editor(
            st.session_state.current_df,
            use_container_width=True,
            num_rows="dynamic",  # 행 추가/삭제 가능
            key="data_editor",
            height=400
        )
        
        # 편집된 데이터를 실시간으로 세션에 반영
        st.session_state.current_df = edited_df
        
        # 현재 편집 중인 파일명 업데이트
        if len(st.session_state.dataframes) > 0:
            current_file_name = list(st.session_state.dataframes.keys())[0] if len(st.session_state.dataframes) == 1 else selected_file
            st.session_state.dataframes[current_file_name] = edited_df
        
        # 데이터 통계 표시
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("총 행 수", len(edited_df))
        with col2:
            st.metric("총 열 수", len(edited_df.columns))
        with col3:
            st.metric("전체 셀 수", len(edited_df) * len(edited_df.columns))
        with col4:
            st.metric("결측값", edited_df.isnull().sum().sum())
        
        st.markdown("---")
          
    # 사이드바 설정
    
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 모델 선택
        st.subheader("🤖 AI 모델 선택")
        model_templates = get_model_templates()
        
        # 모델 카테고리별로 표시
        selected_model = None
        for category_name, models in model_templates.items():
            # 기본적으로 Flagship Chat Models를 확장
            expanded = (category_name == "🚀 Flagship Chat Models")
            with st.expander(category_name, expanded=expanded):
                for model_key, model_info in models.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        model_name = model_info['name']
                        if model_info.get('deprecated', False):
                            st.write(f"**{model_name}** ⚠️")
                            st.caption("⚠️ " + model_info['description'])
                        else:
                            st.write(f"**{model_name}**")
                            st.caption(model_info['description'])
                        
                        # 컨텍스트 윈도우 정보 표시
                        if 'context_window' in model_info:
                            st.caption(f"🔗 컨텍스트: {model_info['context_window']:,} 토큰")
                    
                    with col2:
                        button_disabled = model_info.get('deprecated', False)
                        button_text = "Deprecated" if button_disabled else "선택"
                        if st.button(button_text, key=f"select_{model_key}", disabled=button_disabled):
                            st.session_state.selected_model = model_key
                            st.rerun()
        
        # 현재 선택된 모델 표시
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = "gpt-4o"
        
        current_model = st.session_state.selected_model
        
        # 현재 모델이 deprecated인지 확인
        is_deprecated = False
        for category in model_templates.values():
            if current_model in category:
                is_deprecated = category[current_model].get('deprecated', False)
                break
        
        if is_deprecated:
            st.warning(f"⚠️ 현재 모델: **{current_model}** (Deprecated)")
        else:
            st.success(f"✅ 현재 모델: **{current_model}**")
        
        # 선택된 모델 정보 표시
        for category in model_templates.values():
            if current_model in category:
                model_info = category[current_model]
                
                # 모델 세부 정보를 컨테이너로 묶기
                with st.container():
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Max Tokens", f"{model_info['max_tokens']:,}")
                        if 'context_window' in model_info:
                            st.metric("Context Window", f"{model_info['context_window']:,}")
                    
                    with col2:
                        streaming_status = "✅ 지원" if model_info['supports_streaming'] else "❌ 미지원"
                        st.metric("스트리밍", streaming_status)
                        
                        if 'size' in model_info:
                            st.metric("모델 크기", model_info['size'])
                
                break
        
        st.divider()
        
        # Temperature 설정 (o1 모델은 temperature 미지원)
        if not current_model.startswith("o1"):
            temperature = st.slider(
                "🌡️ Temperature", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.7, 
                step=0.1,
                help="값이 높을수록 더 창의적인 응답을 생성합니다."
            )
        else:
            st.info("🧠 Reasoning 모델은 Temperature 설정을 지원하지 않습니다.")
            temperature = 1.0  # o1 모델의 기본값
        
        st.divider()
        
        # 파일 업로드
        st.header("📂 파일 업로드")
        uploaded_files = st.file_uploader(
            "파일을 선택하세요",
            type=['txt', 'csv', 'xlsx', 'png', 'jpg', 'jpeg', 'gif'],
            accept_multiple_files=True,
            help="텍스트, CSV, Excel(XLSX), 이미지 파일을 업로드할 수 있습니다."
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = []
            for uploaded_file in uploaded_files:
                file_info, df = process_uploaded_file(uploaded_file)
                st.session_state.uploaded_files.append(file_info)
                st.success(f"✅ {uploaded_file.name} 업로드 완료")
                if df is not None:
                    st.info(f"📊 {uploaded_file.name}이 편집 가능한 데이터로 로드되었습니다!")
        
        st.divider()
        
        ## 대화내용 초기화
        ## 대화 메세지 및 파일 초기화
        if st.button("🗑️ 대화 내용 초기화", use_container_width=True):
            st.session_state.messages = []
            st.session_state.uploaded_files = []
            st.session_state.dataframes = {}
            st.session_state.current_df = None
            st.session_state.df_managers = {}
            st.rerun()
        
        # 통계 정보
        st.header("📈 통계")
        st.metric("대화 수", len(st.session_state.messages))
        st.metric("업로드된 파일", len(st.session_state.uploaded_files))
        
        # 모델 카테고리 표시
        current_model = st.session_state.selected_model
        model_category = "알 수 없음"
        for category_name, models in model_templates.items():
            if current_model in models:
                model_category = category_name
                break
        st.metric("모델 카테고리", model_category)
    

    # 메인 채팅 인터페이스
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("💬 메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 데이터 조작 요청 처리
        data_result = None
        result_df = None
        
        # 현재 활성화된 DataFrameManager가 있는지 확인
        current_df_manager = None
        if st.session_state.df_managers:
            # 가장 최근에 업로드된 파일의 매니저 사용
            latest_file = list(st.session_state.df_managers.keys())[-1]
            current_df_manager = st.session_state.df_managers[latest_file]
            
            # 데이터 조작 요청 처리
            data_result, result_df = process_data_request(prompt, current_df_manager)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # 데이터 조작 결과가 있는 경우 먼저 표시
            if data_result and result_df is not None:
                st.markdown(data_result)
                
                # 결과 DataFrame 표시
                st.dataframe(result_df, use_container_width=True)
                
                # 다운로드 버튼 추가
                col1, col2 = st.columns(2)
                
                with col1:
                    # 조작된 결과 DataFrame을 CSV로 변환
                    csv_data = result_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📄 CSV 다운로드",
                        data=csv_data,
                        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key=f"csv_{datetime.now().timestamp()}"
                    )
                
                with col2:
                    # 조작된 결과 DataFrame을 Excel로 변환
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False, sheet_name='Data')
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="📊 Excel 다운로드",
                        data=excel_data,
                        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"xlsx_{datetime.now().timestamp()}"
                    )
                
                full_response = data_result
                
                # 데이터 조작 히스토리 표시
                if current_df_manager and current_df_manager.operation_history:
                    with st.expander("🔍 수행된 작업 히스토리"):
                        for i, operation in enumerate(current_df_manager.operation_history, 1):
                            st.text(f"{i}. {operation}")
            
            else:
                # 일반 AI 응답 처리
                try:
                    response_stream = ai_handler.get_ai_response(
                        st.session_state.messages,
                        model_name=st.session_state.selected_model,
                        temperature=temperature,
                        uploaded_files=st.session_state.uploaded_files
                    )
                    
                    if isinstance(response_stream, str):
                        # 에러 메시지인 경우
                        full_response = response_stream
                        message_placeholder.markdown(full_response)
                    else:
                        # 선택된 모델이 스트리밍을 지원하는지 확인
                        model_templates = get_model_templates()
                        supports_streaming = True
                        for category in model_templates.values():
                            if st.session_state.selected_model in category:
                                supports_streaming = category[st.session_state.selected_model]['supports_streaming']
                                break
                        
                        if supports_streaming:
                            # 스트리밍 응답 처리
                            for chunk in response_stream:
                                if chunk.choices[0].delta.content is not None:
                                    full_response += chunk.choices[0].delta.content
                                    message_placeholder.markdown(full_response + "▌")
                            
                            message_placeholder.markdown(full_response)
                        else:
                            # 비스트리밍 응답 처리 (o1 모델들)
                            with st.spinner("🧠 추론 중입니다... (이 모델은 더 깊이 생각합니다)"):
                                full_response = response_stream.choices[0].message.content
                                message_placeholder.markdown(full_response)
                
                except Exception as e:
                    full_response = f"응답 생성 중 오류가 발생했습니다: {str(e)}"
                    message_placeholder.markdown(full_response)
        
        # AI 메시지 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()