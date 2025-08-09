from dotenv import load_dotenv
from openai import OpenAI
import os


class aiModels:
    def __init__(self):
        load_dotenv()
        API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=API_KEY)


    def get_model_templates(self):
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
    
    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

