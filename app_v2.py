import os, re
import pandas as pd
import streamlit as st
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OPENAI_APIKEY')
client = OpenAI(api_key=API_KEY)

# ---------- 세션 상태 초기화 ----------
if "chat" not in st.session_state:      # 대화 내역
    st.session_state.chat = []
if "df" not in st.session_state:        # 작업할 DataFrame
    st.session_state.df = None
if "fname" not in st.session_state:     # 원본 파일명
    st.session_state.fname = None
# -------------------------------------

st.title("📊 File-Aware Chat CRUD Bot")

# 1) 파일 업로드 -----------------------------------------------------------
uploaded = st.file_uploader(
    "CSV 또는 XLSX 파일을 올려주세요",
    type=["csv", "xlsx"],
    accept_multiple_files=False
)
if uploaded:
    ext = uploaded.name.rsplit(".", 1)[-1].lower()
    if ext == "csv":
        st.session_state.df = pd.read_csv(uploaded)
    else:
        st.session_state.df = pd.read_excel(uploaded)
    st.session_state.fname = uploaded.name
    st.success(f"✅ **{uploaded.name}** 업로드 완료!")

# 2) 데이터 표시 & 직접 편집(옵션) -----------------------------------------
if st.session_state.df is not None:
    st.subheader("🔍 현재 데이터")
    # data_editor → 사용자가 셀, 행 추가/삭제 가능 :contentReference[oaicite:0]{index=0}
    edited_df = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        num_rows="dynamic",
        key="editor"
    )
    st.session_state.df = edited_df  # 실시간 반영

    # 3) 채팅 인터페이스 ---------------------------------------------------
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("데이터 조작 명령을 입력하세요")  # :contentReference[oaicite:1]{index=1}
    if prompt:
        # (1) 화면에 사용자 메시지 표시
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # (2) LLM에게 “pandas 코드만” 요청
        system = (
            "You are a DataFrame assistant. "
            "There is a pandas DataFrame named df. "
            "Translate the user's Korean instruction into **valid, safe pandas code that modifies df in-place**. "
            "Respond ONLY with the code inside a ```python``` block."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content

        # (3) 코드 표시
        st.session_state.chat.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"):          # :contentReference[oaicite:2]{index=2}
            st.markdown(resp)

        # (4) 코드 실행 (아주 제한된 exec)
        code = re.search(r"```python\n([\s\S]+?)```", resp)
        if code:
            try:
                local = {"df": st.session_state.df.copy()}
                exec(code.group(1), {}, local)
                st.session_state.df = local["df"]
                st.success("🔄 데이터 갱신 완료!")
            except Exception as e:
                st.error(f"🚫 코드 실행 오류: {e}")
        else:
            st.error("🚫 유효한 파이썬 코드가 감지되지 않았습니다.")

    # 4) 다운로드 버튼 ------------------------------------------------------
    if st.session_state.df is not None:
        buf = BytesIO()
        if st.session_state.fname and st.session_state.fname.lower().endswith(".csv"):
            st.session_state.df.to_csv(buf, index=False)
            mime, label = "text/csv", "CSV 다운로드"
            file_out = f"edited_{st.session_state.fname}"
        else:
            with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
                st.session_state.df.to_excel(writer, index=False)
            mime, label = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "XLSX 다운로드"
            )
            file_out = f"edited_{(st.session_state.fname or 'file')}.xlsx"
        st.download_button(label, buf.getvalue(), file_out, mime=mime)  # :contentReference[oaicite:3]{index=3}
