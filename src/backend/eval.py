from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from chromadb.config import Settings
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")

embedding = UpstageEmbeddings(
    model="embedding-query",
    api_key=api_key
)

persist_directory = "data/chroma_db"

client_settings = Settings(anonymized_telemetry=False)
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding,
    client_settings=client_settings
)

retriever = vectorstore.as_retriever(
    search_type= 'mmr', # default : similarity(유사도) / mmr 알고리즘
    search_kwargs={"k": 3}
)

from tqdm.notebook import tqdm
from datasets import Dataset
from langchain_upstage import ChatUpstage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

data = {
    "question": [],
    "answer": [],
    "contexts": [],
    "ground_truth": [],
}

llm = ChatUpstage()
prompt_template = PromptTemplate.from_template(
    """
    당신은 의료 전문가를 지원하는 AI 어시스턴트입니다.
    아래 제공된 병원의 환자 기록 문맥(context)를 참고하여, 신규 환자에게 주입해야 할 약물을 추천하세요.

        - 최대한 문맥에 포함된 정보 즉, 이전 환자 사례만을 근거로 약물을 추천하세요.
        - 임의로 정보를 추측하거나, 문맥에 없는 약물을 추천하지 마세요.
        - 약물명, 용량, 투여 경로 등은 명확하게 제시하세요.
        - 부작용, 금기사항 등 주의할 점이 있다면 반드시 함께 안내하세요.
        - 답변은 반드시 한국어로 작성하세요.
        - 만약 추천이 어렵거나 문맥이 부족하다면 "추천이 어렵습니다"라고만 답변하세요.

        ---
        문맥(context): 
        {context}
        ---

        아래의 질문에 답변하세요.
    """
)

def fill_data(data, question, retr):
    results = retr.invoke(question)
    context = [doc.page_content for doc in results]

    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})

    data["question"].append(question)
    data["answer"].append(answer)
    data["contexts"].append(context)
    data["ground_truth"].append("")

# 솔라 논문에서 나올 수 있는 질문 10가지 리스트업
questions = [
    "60세 남성, 체중 78kg, 혈압 155/95mmHg, 맥박 82회/분, 호흡수 18회/분, 체온 36.7℃ 이 환자는 고혈압과 당뇨를 앓고 있습니다. 적절한 혈압 조절 약물을 추천해 주세요.",
    "35세 여성, 체중 62kg, 혈압 120/75mmHg, 맥박 88회/분, 호흡수 20회/분, 체온 38.3℃ 이 환자는 급성 편도염으로 내원했습니다. 사용할 수 있는 항생제를 추천해 주세요.",
    "72세 남성, 체중 70kg, 혈압 140/85mmHg, 맥박 76회/분, 호흡수 19회/분, 체온 36.5℃ 만성 신부전 환자입니다. 사용할 수 있는 통증 조절 약물을 추천해 주세요.",
    "45세 남성, 체중 85kg, 혈압 130/80mmHg, 맥박 70회/분, 호흡수 17회/분, 체온 36.8℃ 심근경색 과거력이 있습니다. 2차 예방을 위한 약물 치료를 제안해 주세요.",
    "28세 임신부, 체중 68kg, 혈압 118/70mmHg, 맥박 90회/분, 호흡수 18회/분, 체온 36.9℃ 빈혈을 호소합니다. 안전하게 사용할 수 있는 철분제를 추천해 주세요.",
    "70세 여성, 체중 54kg, 혈압 135/78mmHg, 맥박 74회/분, 호흡수 18회/분, 체온 36.6℃ 골다공증 진단을 받았습니다. 적절한 약물 치료를 제안해 주세요.",
    "55세 남성, 체중 80kg, 혈압 145/90mmHg, 맥박 85회/분, 호흡수 17회/분, 체온 36.7℃ 고지혈증으로 진단받았습니다. 1차 선택 약물을 추천해 주세요.",
    "40세 여성, 체중 60kg, 혈압 110/68mmHg, 맥박 78회/분, 호흡수 16회/분, 체온 36.5℃ 불면증을 호소합니다. 사용할 수 있는 약물과 주의사항을 안내해 주세요.",
    "65세 남성, 체중 72kg, 혈압 125/75mmHg, 맥박 72회/분, 호흡수 18회/분, 체온 36.6℃ 심부전 진단을 받았습니다. 표준 치료에 포함되는 주요 약물을 추천해 주세요.",
    "50세 여성, 체중 58kg, 혈압 128/82mmHg, 맥박 80회/분, 호흡수 17회/분, 체온 36.7℃ 류마티스 관절염으로 진단받았습니다. 1차 치료에 사용할 수 있는 약물을 추천해 주세요."
]

for question in questions:
    fill_data(data, question, retriever)

dataset = Dataset.from_dict(data)

from ragas.metrics import context_precision, context_recall, faithfulness
from ragas import evaluate
from ragas.run_config import RunConfig

run_config = RunConfig(
    timeout=600,          # 한 번의 작업 최대 대기 시간(초)
    max_retries=20,       # 최대 재시도 횟수 (기본 10, 더 늘릴 수 있음)
    max_wait=600,         # 재시도시 최대 대기 시간(초, 기본 60)
    log_tenacity=True     # 재시도 로그 출력
)

def ragas_evalate(dataset):
    result = evaluate(
        dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
        ],
        llm=llm,
        embeddings=embedding,
        run_config=run_config,
    )
    return result

if __name__ == "__main__":
    result = ragas_evalate(dataset)
    print("평가 결과:")
    print(result)