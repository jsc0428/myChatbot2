import os
from openai import OpenAI
import streamlit as st
from typing import List, Dict, Any, Optional

def get_model_templates() -> Dict[str, Dict[str, Any]]:
    """OpenAI 모델 템플릿 정의 - 2025년 최신 모델 반영"""
    return {
        "🧠 Reasoning Models": {
            "o3": {
                "name": "o3",
                "description": "가장 강력한 추론 모델 (복잡한 수학, 과학, 코딩 문제에 최적화)",
                "max_tokens": 100000,
                "supports_streaming": False,
                "context_window": 200000
            },
            "o4-mini": {
                "name": "o4-mini",
                "description": "빠르고 효율적인 추론 모델 (멀티모달 지원, 도구 통합)",
                "max_tokens": 100000,
                "supports_streaming": False,
                "context_window": 200000
            },
            "o3-mini": {
                "name": "o3-mini",
                "description": "o3의 소형 대안 모델 (추론 능력 유지, 비용 효율적)",
                "max_tokens": 100000,
                "supports_streaming": False,
                "context_window": 200000
            },
            "o1": {
                "name": "o1",
                "description": "이전 o-시리즈 추론 모델 (안정적인 추론 성능)",
                "max_tokens": 100000,
                "supports_streaming": False,
                "context_window": 200000
            },
            "o1-mini": {
                "name": "o1-mini",
                "description": "o1의 소형 대안 (코딩 및 수학 문제에 특화) - Deprecated",
                "max_tokens": 65536,
                "supports_streaming": False,
                "context_window": 128000,
                "deprecated": True
            }
        },
        "🚀 Flagship Chat Models": {
            "gpt-4.1": {
                "name": "gpt-4.1",
                "description": "복잡한 작업을 위한 플래그십 GPT 모델 (최고 성능)",
                "max_tokens": 32768,
                "supports_streaming": True,
                "context_window": 1047576
            },
            "gpt-4o": {
                "name": "gpt-4o",
                "description": "빠르고 지능적이며 유연한 GPT 모델 (멀티모달 지원)",
                "max_tokens": 16384,
                "supports_streaming": True,
                "context_window": 128000
            },
            "gpt-4o-audio": {
                "name": "gpt-4o-audio",
                "description": "GPT-4o 오디오 입출력 지원 모델",
                "max_tokens": 4096,
                "supports_streaming": True,
                "context_window": 128000
            },
            "chatgpt-4o": {
                "name": "chatgpt-4o",
                "description": "ChatGPT에서 사용되는 GPT-4o 모델",
                "max_tokens": 16384,
                "supports_streaming": True,
                "context_window": 128000
            }
        },
        "💡 Cost-Optimized Models": {
            "gpt-4.1-mini": {
                "name": "gpt-4.1-mini",
                "description": "지능성, 속도, 비용의 균형을 맞춘 모델",
                "max_tokens": 32768,
                "supports_streaming": True,
                "context_window": 1047576,
                "size": "Medium"
            },
            "gpt-4.1-nano": {
                "name": "gpt-4.1-nano",
                "description": "가장 빠르고 비용 효율적인 GPT-4.1 모델",
                "max_tokens": 32768,
                "supports_streaming": True,
                "context_window": 1047576,
                "size": "Small"
            },
            "gpt-4o-mini": {
                "name": "gpt-4o-mini",
                "description": "집중된 작업을 위한 빠르고 저렴한 소형 모델",
                "max_tokens": 16384,
                "supports_streaming": True,
                "context_window": 128000,
                "size": "Small"
            },
            "gpt-4o-mini-audio": {
                "name": "gpt-4o-mini-audio",
                "description": "오디오 입출력이 가능한 소형 모델",
                "max_tokens": 4096,
                "supports_streaming": True,
                "context_window": 128000,
                "size": "Small"
            },
            "gpt-3.5-turbo": {
                "name": "gpt-3.5-turbo",
                "description": "빠르고 효율적인 범용 모델 (일반적인 대화에 최적)",
                "max_tokens": 4096,
                "supports_streaming": True,
                "context_window": 16385,
                "size": "Small"
            }
        }
    }

class AIHandler:
    """AI 응답 처리를 위한 클래스"""
    
    def __init__(self, api_key: str):
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
    
    def get_ai_response(self, messages: List[Dict], model_name: str = "gpt-3.5-turbo", 
                       temperature: float = 0.7, uploaded_files: Optional[List] = None):
        """OpenAI API를 사용하여 AI 응답 생성"""
        try:
            model_templates = get_model_templates()
            
            # 선택된 모델의 정보 찾기
            selected_model_info = None
            for category in model_templates.values():
                if model_name in category:
                    selected_model_info = category[model_name]
                    break
            
            if not selected_model_info:
                selected_model_info = {"max_tokens": 1000, "supports_streaming": True}
            
            # 시스템 메시지 추가
            system_message = {
                "role": "system",
                "content": "당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 친절하고 정확하게 답변해주세요. 한국어로 답변해주세요."
            }
            
            # 메시지 구성
            api_messages = [system_message] + messages
            
            # 업로드된 파일이 있는 경우 컨텍스트에 추가
            context_added = False
            if uploaded_files:
                file_context = "\n\n업로드된 파일 정보:\n"
                for file_info in uploaded_files:
                    file_context += f"- {file_info}\n"
                
                if api_messages:
                    api_messages[-1]["content"] += file_context
                    context_added = True
            
            # 현재 편집 중인 DataFrame이 있는 경우 컨텍스트에 추가
            if st.session_state.current_df is not None:
                df_context = "\n\n현재 편집 중인 데이터프레임 정보:\n"
                df_context += f"- 행 수: {len(st.session_state.current_df)}\n"
                df_context += f"- 열 수: {len(st.session_state.current_df.columns)}\n"
                df_context += f"- 컬럼명: {', '.join(st.session_state.current_df.columns.tolist())}\n"
                df_context += f"- 최근 편집된 데이터 (최대 10행):\n{st.session_state.current_df.head(10).to_string()}\n"
                
                if api_messages:
                    if not context_added:
                        api_messages[-1]["content"] += df_context
                    else:
                        api_messages[-1]["content"] += df_context
            
            # API 호출 파라미터 설정
            api_params = {
                "model": model_name,
                "messages": api_messages,
                "max_tokens": selected_model_info["max_tokens"],
            }
            
            # Reasoning 모델의 경우 temperature 지원하지 않음
            if not model_name.startswith("o1"):
                api_params["temperature"] = temperature
            
            # 스트리밍 지원 여부에 따라 설정
            if selected_model_info["supports_streaming"]:
                api_params["stream"] = True
            
            response = self.client.chat.completions.create(**api_params)
            
            return response
        except Exception as e:
            return f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}" 