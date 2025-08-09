# 🤖 AI 챗봇 서비스

Streamlit을 기반으로 한 ChatGPT API 연동 챗봇 서비스입니다.

## ✨ 주요 기능

- 💬 **ChatGPT API 연동**: 실시간으로 OpenAI의 GPT 모델과 대화
- 🤖 **다양한 AI 모델**: Reasoning, GPT, Large/Small 모델 중 선택 가능
- 📄 **파일 업로드**: 텍스트, CSV, 이미지 파일 업로드 및 분석
- 🎛️ **설정 조절**: Temperature 조절로 AI 창의성 제어
- 📊 **대화 통계**: 실시간 대화 통계 및 파일 업로드 현황
- 🎨 **서비스 버튼**: 글쓰기, 정보검색, 아이디어 제안, 데이터 분석 등 빠른 시작 버튼

## 🚀 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정
1. [OpenAI API 키 발급](https://platform.openai.com/api-keys)
2. 프로젝트 폴더에 `.env` 파일 생성
3. 다음 내용을 `.env` 파일에 추가:
```
OPENAI_APIKEY=your_actual_api_key_here
```

### 3. 실행
```bash
streamlit run mychatbot.py
```

## 📱 사용법

1. **웹 인터페이스 접속**: 브라우저에서 `http://localhost:8501` 접속
2. **대화 시작**: 메시지 입력창에 질문을 입력하거나 서비스 버튼 클릭
3. **파일 업로드**: 사이드바에서 파일을 업로드하여 분석 요청
4. **설정 조절**: 사이드바에서 Temperature 조절하여 AI 응답 스타일 변경

## 📂 지원 파일 형식

- **텍스트 파일**: `.txt`
- **CSV 파일**: `.csv`
- **이미지 파일**: `.png`, `.jpg`, `.jpeg`, `.gif`

## 🎯 서비스 버튼 기능

- **📝 글쓰기 도움**: 창의적인 글쓰기 지원
- **🔍 정보 검색**: 정보 검색 및 질의응답
- **💡 아이디어 제안**: 창의적인 아이디어 제안
- **📊 데이터 분석**: 업로드된 데이터 분석 및 해석

## ⚙️ 주요 설정

- **Temperature**: 0.0 (정확한 답변) ~ 1.0 (창의적인 답변)
- **Max Tokens**: 모델별로 자동 설정 (1,000 ~ 65,536)
- **Model**: 다양한 OpenAI 모델 중 선택 가능

## 🤖 지원 모델 (2025년 최신)

### 🧠 Reasoning Models (추론 모델)
- **o3**: 가장 강력한 추론 모델 (복잡한 수학, 과학, 코딩 문제에 최적화)
- **o4-mini**: 빠르고 효율적인 추론 모델 (멀티모달 지원, 도구 통합)
- **o3-mini**: o3의 소형 대안 모델 (추론 능력 유지, 비용 효율적)
- **o1**: 이전 o-시리즈 추론 모델 (안정적인 추론 성능)
- **o1-mini**: o1의 소형 대안 (Deprecated)

### 🚀 Flagship Chat Models (플래그십 채팅 모델)
- **gpt-4.1**: 복잡한 작업을 위한 플래그십 GPT 모델 (최고 성능)
- **gpt-4o**: 빠르고 지능적이며 유연한 GPT 모델 (멀티모달 지원)
- **gpt-4o-audio**: GPT-4o 오디오 입출력 지원 모델
- **chatgpt-4o**: ChatGPT에서 사용되는 GPT-4o 모델

### 💡 Cost-Optimized Models (비용 최적화 모델)
- **gpt-4.1-mini**: 지능성, 속도, 비용의 균형을 맞춘 모델
- **gpt-4.1-nano**: 가장 빠르고 비용 효율적인 GPT-4.1 모델
- **gpt-4o-mini**: 집중된 작업을 위한 빠르고 저렴한 소형 모델
- **gpt-4o-mini-audio**: 오디오 입출력이 가능한 소형 모델
- **gpt-3.5-turbo**: 빠르고 효율적인 범용 모델 (일반적인 대화에 최적)

## 🔧 환경 요구사항

- Python 3.8+
- Streamlit 1.28.0+
- OpenAI API 키

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 