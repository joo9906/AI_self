from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from chromadb.config import Settings

# 1. .env 파일에서 환경변수 불러오기
load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")

# 2. 임베딩 모델 생성 (API 키 전달)
embedding = UpstageEmbeddings(
    model="embedding-query",
    api_key=api_key
)

# 3. 이미 저장된 ChromaDB 경로
persist_directory = "data/chroma_db"  # 크로마DB가 저장된 폴더 경로로 수정

# 4. 저장된 크로마DB에서 벡터스토어 불러오기
client_settings = Settings(anonymized_telemetry=False)
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding,
    client_settings=client_settings
)

def retriever(query, k=3):
    retriever = vectorstore.as_retriever(
        search_type='mmr',
        search_kwargs={"k": k}
    )
    result_docs = retriever.invoke(query)
    return result_docs

def retriever_with_score(query, k=5):
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results

if __name__ == "__main__":
    query = input("검색할 쿼리를 입력하세요: ")
    results = retriever_with_score(query)
    print("\n[검색 결과]")
    for i, doc in enumerate(results, 1):
        print(f"\n--- 문서 {i} ---")
        # doc이 dict 또는 Document 객체일 수 있으니, 적절히 출력
        print(doc[0].page_content)
