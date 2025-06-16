import streamlit as st
from typing import List
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OPENAI_APIKEY')

# 채팅 기록을 저장할 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("AI 챗봇 서비스 💬")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("설정")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1,
                              help="값이 높을수록 더 창의적인 응답을 생성합니다.")
        st.divider()
        if st.button("대화 내용 초기화"):
            st.session_state.messages = []
            st.rerun()
    
    # 메인 채팅 인터페이스
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = "현재는 더미 응답입니다. 실제 LLM 서비스와 연동이 필요합니다."
            
            # 타이핑되는 효과 구현
            for chunk in range(len(full_response)):
                time.sleep(0.05)
                message_placeholder.markdown(full_response[:chunk+1] + "▌")
            message_placeholder.markdown(full_response)
            
        # AI 메시지 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()