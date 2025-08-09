import pandas as pd
import base64
from typing import Tuple, Optional
from data_manager import DataFrameManager
import streamlit as st

def encode_image(image_file):
    """이미지 파일을 base64로 인코딩"""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def process_uploaded_file(uploaded_file) -> Tuple[str, Optional[pd.DataFrame]]:
    """업로드된 파일을 처리하고 텍스트로 변환"""
    try:
        if uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8"), None
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            # DataFrame을 세션에 저장
            st.session_state.dataframes[uploaded_file.name] = df
            st.session_state.current_df = df
            
            # DataFrameManager 인스턴스 생성
            df_manager = DataFrameManager(df, uploaded_file.name)
            if "df_managers" not in st.session_state:
                st.session_state.df_managers = {}
            st.session_state.df_managers[uploaded_file.name] = df_manager
            
            # DataFrame 기본 정보 제공
            info = f"CSV 파일 분석 결과 - {uploaded_file.name}:\n"
            info += f"- 행 수: {len(df)}\n"
            info += f"- 열 수: {len(df.columns)}\n"
            info += f"- 컬럼명: {', '.join(df.columns.tolist())}\n"
            info += f"- 데이터 타입:\n{df.dtypes.to_string()}\n\n"
            info += f"첫 5행 미리보기:\n{df.head().to_string()}\n\n"
            if len(df) > 5:
                info += f"마지막 5행 미리보기:\n{df.tail().to_string()}\n\n"
            info += f"기술통계:\n{df.describe().to_string()}"
            return info, df
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # XLSX 파일 처리
            df = pd.read_excel(uploaded_file)
            # DataFrame을 세션에 저장
            st.session_state.dataframes[uploaded_file.name] = df
            st.session_state.current_df = df
            
            # DataFrameManager 인스턴스 생성
            df_manager = DataFrameManager(df, uploaded_file.name)
            if "df_managers" not in st.session_state:
                st.session_state.df_managers = {}
            st.session_state.df_managers[uploaded_file.name] = df_manager
            
            # DataFrame 기본 정보 제공
            info = f"XLSX 파일 분석 결과 - {uploaded_file.name}:\n"
            info += f"- 행 수: {len(df)}\n"
            info += f"- 열 수: {len(df.columns)}\n"
            info += f"- 컬럼명: {', '.join(df.columns.tolist())}\n"
            info += f"- 데이터 타입:\n{df.dtypes.to_string()}\n\n"
            info += f"첫 5행 미리보기:\n{df.head().to_string()}\n\n"
            if len(df) > 5:
                info += f"마지막 5행 미리보기:\n{df.tail().to_string()}\n\n"
            info += f"기술통계:\n{df.describe().to_string()}"
            return info, df
        elif uploaded_file.type in ["image/jpeg", "image/png", "image/gif"]:
            return f"이미지 파일이 업로드되었습니다: {uploaded_file.name}", None
        else:
            return f"지원되지 않는 파일 형식입니다: {uploaded_file.type}", None
    except Exception as e:
        return f"파일 처리 중 오류가 발생했습니다: {str(e)}", None 