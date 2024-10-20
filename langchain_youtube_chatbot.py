# 설치 명령어는 다음과 같습니다.
# pip install langchain==0.2.1 langchain_openai==0.1.19 langchain-core==0.2.24 openai==1.37.1 langchain_community==0.2.1 youtube-transcript-api tiktoken faiss-cpu google-search-results

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
import textwrap
import os

# 1. API Key 설정 (환경 변수 설정 대신 키 직접 설정)
OPENAI_API_KEY = "OPENAI_API_KEY"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 2. Youtube에서 transcript 가져와 임베딩 후 벡터DB에 저장하는 함수
def create_db_from_youtube_video_url(video_url, lang='en'):
    loader = YoutubeLoader.from_youtube_url(video_url, language=lang)  # Youtube URL 입력
    transcript = loader.load()  # 전체 transcript를 얻어온다
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # 받아온 transcript를 잘라냄
    docs = text_splitter.split_documents(transcript)
    
    embeddings = OpenAIEmbeddings()  # 임베딩 모델
    db = FAISS.from_documents(docs, embeddings)  # 텍스트를 벡터로 변환해 DB에 넣음
    return db, docs

# 3. Youtube 내용에 대해 질문하고 답변을 얻는 함수
def get_response_from_query(db, query, k=2):
    docs = db.similarity_search(query, k=k)  # 유사성 검색 수행
    docs_page_content = " ".join([d.page_content for d in docs])  # 유사성 높은 문서 결합

    # 시스템 메시지 프롬프트
    system_template = """
        You are a helpful assistant who answers questions about YouTube videos based on their transcripts. {docs}
        Please only use factual information from the transcript to answer the question. If there's insufficient information, respond with "I don't know".
    """
    system_message_prompt = ChatPromptTemplate.from_template(system_template)

    # 사용자 질문 프롬프트
    human_template = "Question: {question}"
    human_message_prompt = ChatPromptTemplate.from_template(human_template)

    # ChatGPT와 함께 사용하는 RunnableSequence 생성
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
    sequence = system_message_prompt | human_message_prompt | chat
    
    # 응답을 invoke로 호출하여 얻음
    response = sequence.invoke({
        "question": query,
        "docs": docs_page_content
    })
    # Access the content of the AIMessage using response.content
    return response.content.replace("\n", ""), docs 

# 4. 테스트 실행
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=GagsR5-bdLs"
    lang = "en"  # 언어 설정
    db, docs = create_db_from_youtube_video_url(video_url, lang=lang)
    
    # 질문
    query = "How many rounds is this?"
    response, docs = get_response_from_query(db, query)
    print(textwrap.fill(response, width=50))
    
    