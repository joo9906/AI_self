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

persist_directory = "data/chroma_db_v2"

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
    아래 제공된 병원의 환자 기록 문맥(context)을 참고하여, 신규 환자에게 주입해야 할 약물을 추천하세요.

    - 최대한 문맥에 포함된 정보 즉, 이전 환자 사례만을 근거로 약물을 추천하세요.
    - 임의로 정보를 추측하거나, 문맥에 없는 약물을 추천하지 마세요.
    - 반드시 약물명, 용량, 투여 경로 등은 명확하게 제시하세요.
    - 부작용, 금기사항 등 주의할 점이 있다면 반드시 함께 안내하세요.
    - 답변은 반드시 한국어로 작성하세요.
    - 만약 추천이 어렵거나 문맥이 부족하다면 "추천이 어렵습니다"라고만 답변하세요.
    - 반드시 약물을 제안 할때만 예시 답변과 유사한 형식으로 답변하세요.
    예시 답변:
    **약물: 에피네프린(epinephrine)**
    **용량**: 0.3-0.5 mg (0.3-0.5 mL of 1:1000 solution)
    **투여 경로**: 근육주사(IM) 또는 피하주사(SC)
    **부작용**: 심박수 증가, 불안, 떨림, 두통 등
    **금기사항**: 심혈관계 질환 환자에게는 주의가 필요합니다.
    **주의사항**: 주입 후 환자의 상태를 지속적으로 모니터링하고, 필요시 추가 투여를 고려하세요.
    **제안 이유**
    - 이 약물은 아나필락시스(심한 알레르기 반응)에 대한 표준 치료제로, 빠른 효과가 있습니다.
    - 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
    - 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.

    ---
    문맥(context): 
    {context}
    ---
    """
)

def fill_data(data, question, retr, answers):
    results = retr.invoke(question)
    context = [doc.page_content for doc in results]

    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})

    data["question"].append(question)
    data["answer"].append(answer)
    data["contexts"].append(context)
    data["ground_truth"].append("")

# 테스트 질문 10가지 리스트업
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

answers = [
    """**약물:** 암로디핀(amlodipine)
**용량:** 5~10mg 1일 1회
**투여 경로:** 경구(PO)
**부작용:** 부종, 두통, 안면홍조, 어지러움 등
**금기사항:** 중증 저혈압 환자, 심부전 환자 등은 주의 필요
**주의사항:** 혈압과 부작용을 정기적으로 관찰하고, 용량 조절이 필요할 수 있습니다.
**제안 이유**
- 고혈압 환자에게 칼슘채널차단제는 1차 선택 약물로 널리 사용됩니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 아목시실린-클라불라네이트(amoxicillin-clavulanate)
**용량:** 500/125mg 1일 3회, 7~10일간
**투여 경로:** 경구(PO)
**부작용:** 위장장애, 설사, 알레르기 반응 등
**금기사항:** 페니실린계 항생제 알레르기 환자
**주의사항:** 알레르기 반응 발생 시 즉시 투약 중단, 충분한 수분 섭취 권장
**제안 이유**
- 급성 편도염의 1차 치료제이며, 효과와 안전성이 입증되어 있습니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 아세트아미노펜(acetaminophen)
**용량:** 500~1000mg 4~6시간마다 필요시(1일 최대 4g)
**투여 경로:** 경구(PO)
**부작용:** 간독성(과량 복용 시), 발진 등
**금기사항:** 중증 간질환 환자
**주의사항:** 용량을 초과하지 않도록 주의, 간기능 모니터링 필요
**제안 이유**
- 만성 신부전 환자에서 비교적 안전하게 사용할 수 있는 진통제입니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 아스피린(aspirin), 아토르바스타틴(atorvastatin), 베타차단제(beta-blocker), ACE 억제제(ACE inhibitor)
**용량:** 아스피린 100mg 1일 1회, 아토르바스타틴 20mg 1일 1회 등
**투여 경로:** 경구(PO)
**부작용:** 출혈, 근육통, 저혈압, 기침 등(약물별 상이)
**금기사항:** 각 약물별 금기사항(예: 아스피린 알레르기, 중증 간질환 등)
**주의사항:** 약물 상호작용 및 부작용 모니터링 필요, 정기적 검진 권장
**제안 이유**
- 심근경색 2차 예방을 위한 표준 약물 조합입니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 푸마르산 철분(ferrous fumarate)
**용량:** 100~200mg(철분 기준) 1일 1~2회
**투여 경로:** 경구(PO)
**부작용:** 위장장애, 변비, 흑색변 등
**금기사항:** 철 과다증, 혈색소증 환자
**주의사항:** 식사 전 복용 권장, 위장장애 발생 시 식후 복용, 다른 약물과 시간차 두고 복용
**제안 이유**
- 임신부에서 안전하게 사용할 수 있는 철분제입니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 알렌드로네이트(alendronate)
**용량:** 70mg 1주 1회
**투여 경로:** 경구(PO)
**부작용:** 소화불량, 식도염, 근골격계 통증 등
**금기사항:** 식도운동장애, 저칼슘혈증 환자
**주의사항:** 복용 후 최소 30분간 눕지 않기, 충분한 물과 함께 복용
**제안 이유**
- 골다공증 치료에 1차로 권장되는 비스포스포네이트 계열 약물입니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 아토르바스타틴(atorvastatin)
**용량:** 10~20mg 1일 1회
**투여 경로:** 경구(PO)
**부작용:** 근육통, 간기능 이상, 소화불량 등
**금기사항:** 중증 간질환 환자, 임신부
**주의사항:** 간기능 정기적 검사, 근육통 발생 시 즉시 보고
**제안 이유**
- 고지혈증의 1차 선택 약물로 스타틴 계열이 권장됩니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 졸피뎀(zolpidem)
**용량:** 5~10mg 취침 전 1회
**투여 경로:** 경구(PO)
**부작용:** 어지러움, 졸림, 기억장애, 낙상 위험 등
**금기사항:** 중증 간질환, 알코올 남용 환자
**주의사항:** 운전 등 위험한 작업 금지, 장기 복용 피하기
**제안 이유**
- 불면증 치료에 효과적이며, 단기간 사용에 적합한 약물입니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 엔알라프릴(enalapril)
**용량:** 2.5~20mg 1일 1~2회
**투여 경로:** 경구(PO)
**부작용:** 저혈압, 기침, 신기능 저하 등
**금기사항:** 임신부, 혈관부종 병력 환자
**주의사항:** 신기능 및 전해질 정기적 검사, 저혈압 주의
**제안 이유**
- 심부전 표준 치료에 ACE 억제제가 포함됩니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다.""",

    """**약물:** 메토트렉세이트(methotrexate)
**용량:** 7.5~15mg 1주 1회
**투여 경로:** 경구(PO) 또는 피하주사(SC)
**부작용:** 간기능 이상, 구역, 구토, 골수억제 등
**금기사항:** 임신부, 간질환, 신질환 환자
**주의사항:** 간기능 및 혈액검사 정기적 실시, 임신 피하기
**제안 이유**
- 류마티스 관절염의 1차 치료 약물로 널리 사용됩니다.
- 환자의 상태와 문맥에 기반하여, 이 약물이 가장 적합하다고 판단됩니다.
- 이전 환자 사례에서도 유사한 상황에서 효과적인 결과를 보였습니다."""
]


for i in range(len(questions)):
    fill_data(data, questions[i], retriever, answers[i])

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