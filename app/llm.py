# langchain을 통해 OpenAI LLM 호출 관련 클래스들 임포트
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 환경변수 
import os
from dotenv import load_dotenv

# .env 파일에서 OPENAI_API_KEY 등을 불러옴
load_dotenv()


# model="gpt-4o"로 지정 -> 변경필요한지..? 
# 분석결과의 일관성을 위해 temperature는 0.3으로 설정 -> 변경필요한지..?
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)


def run_final_llm_review(error_message: str, docs: str) -> str:
    prompt = f"""
            너는 Oracle/MySQL/MSSQL 전문 데이터베이스 에러 분석가야.

            에러 메시지는 다음과 같아:
            {error_message}

            유사도 기반으로 검색된 문서들은 아래와 같아:
            {docs}


            이 문서들이 이 에러에 적합한 대응문서인지 평가해.
            적합한 내용이라면 그대로 docs를 사용용하고, 만약 잘못된 내용이 있다면, 정확한 *원인*과 *해결방안*을 다시 정리해서 제시해줘.
            해결방안과 원인을 제시할때는 벤더사 문서를 기반으로 분석 및 정리해줘.
            존댓말로 답변 해주고,  slack 형식에 맞춰서 반환해줘.
            최종 반환하기 전에 **두개가 덜어간곳은 *하나로 변경해줘.
            항상 아래와 같은 포맷으로 답변해:

            *발생에러*\n    

            *원인*\n

            *해결방안*\n
    
             """

    # LLM 호출
    response = llm.invoke([
        SystemMessage(content="너는전문 데이터베이스 에러 분석가야."),
        HumanMessage(content=prompt)
    ])

    return response.content


