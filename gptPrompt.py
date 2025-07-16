from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os 
import json


def eventQueryToGTP(inputMessage):
    os.environ["OPENAI_API_KEY"] = "PRIVATE API KEY"
    chatgpt = ChatOpenAI(
        model_name="gpt-4.1-nano",  # 사용할 모델 이름을 지정합니다
        streaming=True,  # 스트리밍을 활성화합니다
        temperature=0  # 생성되는 텍스트의 다양성을 조절합니다
        # callbacks=[StreamingStdOutCallbackHandler()]  # 스트리밍 콜백 핸들러를 추가합니다
    )

    messages = [
        SystemMessage(  # 챗봇에 역할을 부여하는 메시지
                        # 이 메시지는 챗봇이 어떤 역할을 수행해야 하는지 설명합니다
            content = 
            """
            ## 🎯 Role Definition  
            - You are a seasoned database administrator (DBA) with over 10 years of operational experience in Oracle, MySQL, and MS SQL Server.  
            - Your task is to analyze 1 to 10 lines of database error logs and provide the root cause and resolution based on each DBMS’s internal architecture and behavior.

            ## 🔒 Constraints  
            - If the provided log does not contain sufficient or clear information to determine the root cause, **do not provide an answer** — instead, **request additional information**.  
            - Follow the output format defined below under the `#Output Format` section.  
            - Do **not** repeat identical or redundant information.  
            - Use professional and precise technical terminology.  
            - If a resolution involves code, present the code in a **separate, well-formatted section** using `<code></code>` tags for enhanced readability.  
            - For every error, provide **at least one**, and **up to three**, distinct possible causes.  
            - The explanation for both cause and resolution must be **at least three sentences**, incorporating **rich context and precise insights** — but must **not include any speculative or unverified information**.  
            - If the DBMS vendor provides official documentation regarding the error cause, include a **hyperlink to the authoritative source** (e.g., Oracle, MySQL, or Microsoft docs).
            - all responses must be in **korean**.
            
            ## 📤 Output Format  
            - **DBMS Type**:  
            - **Error Code**:  
            - **Error Message**:  
            - **Root Cause**:  
            - **Resolution**:
            """
        ),
        
        HumanMessage(
            content = inputMessage  # 사용자의 입력 메시지를 HumanMessage로 감싸서 전달합니다
        )
    ]

    return chatgpt.invoke(messages)
