import pandas as pd
import io
import re
from typing import Union, List, Tuple, Optional
from datetime import datetime

class DataFrameManager:
    """데이터프레임 조작 및 관리를 위한 클래스"""
    
    def __init__(self, df: pd.DataFrame, name: str = "data"):
        self.original_df = df.copy()  # 원본 데이터 보존
        self.current_df = df.copy()   # 현재 작업 중인 데이터
        self.name = name
        self.operation_history = []   # 작업 히스토리
    
    def get_top_k(self, k: int = 10) -> pd.DataFrame:
        """상위 k개 데이터 반환"""
        result_df = self.current_df.head(k)
        self.operation_history.append(f"상위 {k}개 데이터 조회")
        return result_df
    
    def get_bottom_k(self, k: int = 10) -> pd.DataFrame:
        """하위 k개 데이터 반환"""
        result_df = self.current_df.tail(k)
        self.operation_history.append(f"하위 {k}개 데이터 조회")
        return result_df
    
    def filter_by_column(self, column: str, condition: str, method: str = "contains") -> pd.DataFrame:
        """특정 컬럼의 조건에 따라 데이터 필터링"""
        if column not in self.current_df.columns:
            raise ValueError(f"컬럼 '{column}'이 존재하지 않습니다.")
        
        try:
            if method == "contains":
                # 대소문자 구분 없이 포함 여부 확인
                result_df = self.current_df[self.current_df[column].astype(str).str.contains(condition, case=False, na=False)]
            elif method == "equals":
                result_df = self.current_df[self.current_df[column] == condition]
            elif method == "startswith":
                result_df = self.current_df[self.current_df[column].astype(str).str.startswith(condition, na=False)]
            elif method == "endswith":
                result_df = self.current_df[self.current_df[column].astype(str).str.endswith(condition, na=False)]
            else:
                result_df = self.current_df[self.current_df[column].astype(str).str.contains(condition, case=False, na=False)]
            
            self.operation_history.append(f"'{column}' 컬럼에서 '{condition}' 조건으로 필터링 ({method})")
            return result_df
        except Exception as e:
            raise ValueError(f"필터링 중 오류 발생: {str(e)}")
    
    def drop_columns(self, columns: Union[str, List[str]]) -> pd.DataFrame:
        """특정 컬럼 삭제 (원본 유지)"""
        if isinstance(columns, str):
            columns = [columns]
        
        missing_cols = [col for col in columns if col not in self.current_df.columns]
        if missing_cols:
            raise ValueError(f"존재하지 않는 컬럼: {missing_cols}")
        
        result_df = self.current_df.drop(columns=columns)
        self.operation_history.append(f"컬럼 삭제: {columns}")
        return result_df
    
    def drop_rows(self, indices: Union[int, List[int]]) -> pd.DataFrame:
        """특정 행 삭제 (원본 유지)"""
        if isinstance(indices, int):
            indices = [indices]
        
        # 인덱스 범위 확인
        valid_indices = [idx for idx in indices if idx in self.current_df.index]
        if not valid_indices:
            raise ValueError("유효한 인덱스가 없습니다.")
        
        result_df = self.current_df.drop(index=valid_indices)
        self.operation_history.append(f"행 삭제: 인덱스 {valid_indices}")
        return result_df
    
    def sort_by_column(self, column: str, ascending: bool = True) -> pd.DataFrame:
        """특정 컬럼 기준으로 정렬"""
        if column not in self.current_df.columns:
            raise ValueError(f"컬럼 '{column}'이 존재하지 않습니다.")
        
        result_df = self.current_df.sort_values(by=column, ascending=ascending)
        order_text = "오름차순" if ascending else "내림차순"
        self.operation_history.append(f"'{column}' 컬럼 기준 {order_text} 정렬")
        return result_df
    
    def update_current_df(self, new_df: pd.DataFrame):
        """현재 작업 중인 데이터프레임 업데이트"""
        self.current_df = new_df.copy()
    
    def reset_to_original(self):
        """원본 데이터로 복원"""
        self.current_df = self.original_df.copy()
        self.operation_history.append("원본 데이터로 복원")
    
    def get_info(self) -> str:
        """데이터프레임 정보 반환"""
        info = f"데이터셋: {self.name}\n"
        info += f"행 수: {len(self.current_df)}\n"
        info += f"열 수: {len(self.current_df.columns)}\n"
        info += f"컬럼: {', '.join(self.current_df.columns.tolist())}\n"
        if self.operation_history:
            info += f"수행한 작업:\n" + "\n".join([f"- {op}" for op in self.operation_history[-5:]])  # 최근 5개 작업만 표시
        return info
    
    def to_csv(self) -> bytes:
        """CSV 형태로 변환"""
        return self.current_df.to_csv(index=False).encode('utf-8-sig')
    
    def to_excel(self) -> bytes:
        """Excel 형태로 변환"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            self.current_df.to_excel(writer, index=False, sheet_name='Data')
        return output.getvalue()

def process_data_request(user_input: str, df_manager: DataFrameManager) -> Tuple[Optional[str], Optional[pd.DataFrame]]:
    """사용자의 데이터 조작 요청을 처리"""
    user_input_lower = user_input.lower()
    
    try:
        # 사용 가능한 작업 안내 요청
        if any(keyword in user_input_lower for keyword in ['할 수 있는', '가능한', '작업', '명령어', '기능']):
            guide_text = f"""
## 📊 **데이터 조작 가능한 명령어들**

현재 로드된 데이터: **{df_manager.name}**
- 행 수: {len(df_manager.current_df)}
- 열 수: {len(df_manager.current_df.columns)}
- 컬럼: {', '.join(df_manager.current_df.columns.tolist())}

### 🔍 **데이터 조회**
- `상위 10개 데이터 보여줘` 또는 `top 5`
- `하위 10개 데이터 보여줘` 또는 `bottom 3`

### 🎯 **데이터 필터링**
- `[컬럼명]에서 [키워드] 포함된 데이터만`
- `job_title에서 AI 관련 데이터만`
- `salary에서 100000 이상`

### 🗑️ **데이터 삭제**
- `[컬럼명] 컬럼 삭제해줘`
- `불필요한 컬럼 제거`

### 📈 **데이터 정렬**
- `[컬럼명] 기준으로 정렬해줘`
- `salary 내림차순으로 정렬`
- `이름 오름차순 정렬`

### 📥 **데이터 다운로드**
모든 조작된 결과는 **CSV** 또는 **Excel** 형태로 다운로드 가능합니다!
            """
            return guide_text, df_manager.current_df.head(5)
        
        # Top-K 데이터 요청
        top_match = re.search(r'(?:상위|top)\s*(\d+)', user_input_lower)
        if top_match:
            k = int(top_match.group(1))
            result_df = df_manager.get_top_k(k)
            return f"상위 {k}개 데이터를 보여드립니다:", result_df
        
        # Bottom-K 데이터 요청
        bottom_match = re.search(r'(?:하위|bottom)\s*(\d+)', user_input_lower)
        if bottom_match:
            k = int(bottom_match.group(1))
            result_df = df_manager.get_bottom_k(k)
            return f"하위 {k}개 데이터를 보여드립니다:", result_df
        
        # 숫자 범위 필터링 (예: "salary 100000 이상")
        number_pattern = r'(\d+)\s*(?:이상|이하|초과|미만|>=|<=|>|<)'
        number_match = re.search(number_pattern, user_input)
        if number_match:
            value = float(number_match.group(1))
            operator = user_input[number_match.end()-2:number_match.end()]
            
            for column in df_manager.current_df.columns:
                if column.lower() in user_input_lower:
                    try:
                        if '이상' in user_input or '>=' in user_input:
                            result_df = df_manager.current_df[pd.to_numeric(df_manager.current_df[column], errors='coerce') >= value]
                        elif '이하' in user_input or '<=' in user_input:
                            result_df = df_manager.current_df[pd.to_numeric(df_manager.current_df[column], errors='coerce') <= value]
                        elif '초과' in user_input or '>' in user_input:
                            result_df = df_manager.current_df[pd.to_numeric(df_manager.current_df[column], errors='coerce') > value]
                        elif '미만' in user_input or '<' in user_input:
                            result_df = df_manager.current_df[pd.to_numeric(df_manager.current_df[column], errors='coerce') < value]
                        
                        if not result_df.empty:
                            df_manager.operation_history.append(f"'{column}' 컬럼 숫자 조건 필터링: {value}")
                            return f"'{column}' 컬럼에서 조건에 맞는 데이터를 필터링했습니다:", result_df
                    except:
                        continue
        
        # 컬럼 필터링 요청 (개선된 버전)
        for column in df_manager.current_df.columns:
            column_lower = column.lower()
            if column_lower in user_input_lower:
                # AI, 인공지능, 머신러닝 등의 키워드 검색
                ai_keywords = ['ai', '인공지능', '머신러닝', 'machine learning', 'data scientist', 'ml', 'artificial intelligence']
                for keyword in ai_keywords:
                    if keyword in user_input_lower:
                        result_df = df_manager.filter_by_column(column, keyword)
                        if not result_df.empty:
                            return f"'{column}' 컬럼에서 '{keyword}' 관련 데이터를 필터링했습니다:", result_df
                
                # "포함된", "관련된" 등의 키워드와 함께 사용되는 조건 추출
                patterns = [
                    rf"{column_lower}.*?(?:포함|관련|해당).*?([가-힣a-z0-9\s]+)",
                    rf"([가-힣a-z0-9\s]+).*?{column_lower}",
                    rf"{column_lower}.*?([가-힣a-z0-9\s]+)"
                ]
                
                for pattern in patterns:
                    filter_match = re.search(pattern, user_input_lower)
                    if filter_match:
                        condition = filter_match.group(1).strip()
                        # 불용어 제거
                        stop_words = ['에서', '의', '을', '를', '이', '가', '으로', '에', '만', '데이터', '컬럼', '값']
                        for stop_word in stop_words:
                            condition = condition.replace(stop_word, '').strip()
                        
                        if condition and len(condition) > 1:
                            result_df = df_manager.filter_by_column(column, condition)
                            if not result_df.empty:
                                return f"'{column}' 컬럼에서 '{condition}' 조건으로 필터링했습니다:", result_df
        
        # 컬럼 삭제 요청
        if any(keyword in user_input for keyword in ['삭제', 'delete', '제거', '빼']):
            for column in df_manager.current_df.columns:
                if column.lower() in user_input_lower:
                    result_df = df_manager.drop_columns(column)
                    return f"'{column}' 컬럼을 삭제했습니다:", result_df
        
        # 행 삭제 요청 (인덱스 기반)
        row_delete_match = re.search(r'(\d+)(?:번째|행|줄).*?삭제', user_input)
        if row_delete_match:
            row_index = int(row_delete_match.group(1)) - 1  # 사용자는 1부터 시작
            if 0 <= row_index < len(df_manager.current_df):
                result_df = df_manager.drop_rows(row_index)
                return f"{row_index + 1}번째 행을 삭제했습니다:", result_df
        
        # 정렬 요청
        if any(keyword in user_input for keyword in ['정렬', 'sort', '순서']):
            for column in df_manager.current_df.columns:
                if column.lower() in user_input_lower:
                    ascending = any(keyword in user_input for keyword in ['오름차순', 'asc', '낮은', '작은'])
                    descending = any(keyword in user_input for keyword in ['내림차순', 'desc', '높은', '큰'])
                    order = True if ascending else False if descending else True
                    result_df = df_manager.sort_by_column(column, ascending=order)
                    order_text = "오름차순" if order else "내림차순"
                    return f"'{column}' 컬럼 기준으로 {order_text} 정렬했습니다:", result_df
        
        # 원본 데이터로 복원 요청
        if any(keyword in user_input_lower for keyword in ['원본', '복원', '초기화', 'reset']):
            df_manager.reset_to_original()
            return "원본 데이터로 복원했습니다:", df_manager.current_df
        
        return None, None
        
    except Exception as e:
        return f"데이터 처리 중 오류가 발생했습니다: {str(e)}", None 