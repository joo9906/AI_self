# chat.py
from dotenv import load_dotenv
import os
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 환경 변수 로드 및 LLM 세팅
load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")
llm = ChatUpstage(api_key=api_key, model="solar-pro", temperature=0.7, max_tokens=1024)

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            당신은 의료 전문가를 지원하는 AI 어시스턴트입니다.
            아래 제공된 병원의 환자 기록 문맥(context)과 지금까지의 대화의 히스토리(history)를 참고하여, 신규 환자에게 주입해야 할 약물을 추천하세요.

            - 최대한 문맥에 포함된 정보 즉, 이전 환자 사례만을 근거로 약물을 추천하세요.
            - 임의로 정보를 추측하거나, 문맥에 없는 약물을 추천하지 마세요.
            - 약물명, 용량, 투여 경로 등은 명확하게 제시하세요.
            - 부작용, 금기사항 등 주의할 점이 있다면 반드시 함께 안내하세요.
            - 답변은 반드시 한국어로 작성하세요.
            - 만약 추천이 어렵거나 문맥이 부족하다면 "추천이 어렵습니다"라고만 답변하세요.
            ---
            대화의 히스토리(history): 
            {history}
            ---
            문맥(context): 
            {context}
            ---
            아래의 질문에 답변하세요.
            """,
        ),
        ("human", "{input}"),
    ]
)
output_parser = StrOutputParser()

# 세션별 히스토리/컨텍스트 저장 (프로세스 메모리)
session_histories = {}
session_contexts = {}

def get_message_history(session_id: str):
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

def chat(session_id: str, query: str, context: str = None):
    # context가 주어지면(최초 대화), 세션에 저장
    if context is not None:
        session_contexts[session_id] = context
    # context가 없으면 기존 세션의 context 사용
    context = session_contexts.get(session_id, "")
    print(f"Session ID: {session_id}\n Query: {query}\n Context: {context[0].page_content}")
    chain = RunnableWithMessageHistory(
        prompt | llm | output_parser,
        get_message_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    response = chain.invoke(
        {"context": context, "input": query},
        config={"configurable": {"session_id": session_id}}
    )
    return response
