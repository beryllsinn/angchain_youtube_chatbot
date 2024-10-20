# 유튜브 동영상 기반 챗봇

이 프로젝트는 유튜브 동영상의 자막 데이터를 활용하여 질문에 답변하는 **챗봇**입니다. LangChain과 OpenAI API를 사용하여, 유튜브 자막 데이터를 기반으로 사용자의 질문에 응답합니다.

## 기능

- **유튜브 동영상 자막 추출**: `YoutubeLoader`를 사용하여 동영상의 자막을 가져옵니다.
- **텍스트 분리**: `RecursiveCharacterTextSplitter`를 통해 자막 텍스트를 분리하여 처리합니다.
- **임베딩 및 유사성 검색**: `OpenAIEmbeddings`와 `FAISS`를 사용하여 텍스트 데이터를 임베딩하고, 유사한 문서를 검색하여 답변을 제공합니다.
- **질문/응답 시스템**: OpenAI의 GPT-3.5를 활용해 유튜브 자막을 기반으로 질문에 답변을 생성합니다.

## 설치 방법

1. **필요한 라이브러리 설치**:

   아래 명령어로 프로젝트에 필요한 라이브러리를 설치할 수 있습니다.

   ```bash
   pip install langchain-openai youtube-transcript-api tiktoken faiss-cpu
   ```

2. **환경 변수 설정**:

   API 키를 안전하게 관리하기 위해, 환경 변수로 설정합니다.
    `OPENAI_API_KEY` 환경 변수에 OpenAI API 키를 설정해야 합니다.

   **Windows**:
   ```bash
   set OPENAI_API_KEY=your-openai-api-key
   ```

   **macOS/Linux**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   또는 `.env` 파일을 만들어 API 키를 저장할 수 있습니다.

   `.env` 파일 예시:
   ```plaintext
   OPENAI_API_KEY=your-openai-api-key
   ```

## 사용 방법

1. **유튜브 동영상 URL 설정**:
   
   `video_url` 변수에 분석할 유튜브 동영상의 URL을 입력합니다.

   ```python
   video_url = "https://www.youtube.com/watch?v=example"
   ```

2. **질문하기**:

   코드를 실행하면 챗봇이 유튜브 자막을 분석하고 사용자가 입력한 질문에 응답합니다.


3. **결과 확인**:

   질문에 대한 답변이 터미널에 출력됩니다.


## 주의사항

- 유튜브 동영상의 자막이 제대로 제공되지 않으면 챗봇이 정확한 답변을 제공하지 못할 수 있습니다.
- 챗봇은 동영상의 자막에만 의존하므로, 자막에 포함된 정보 이상을 답변할 수 없습니다.
