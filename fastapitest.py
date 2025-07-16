import os
import requests
from slack_sdk import WebClient
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from langchainCallbackStreaming import eventQueryToGTP

# """ErrorCode 145: SQLPREVENTFULLSCAN class parameter is 1 for this table. Query that performs full scan of data map is not allowed"""
# Initialize FastAPI app
app = FastAPI()

# 슬랙 설정 
SLACK_TOKEN = "SLACK_TOKEN" 
CHANNEL_ID = "CHANNEL_ID"  

client = WebClient(token=SLACK_TOKEN)

# SLACK slash command 핸들러로 부터 데이터를 받아서 처리 
# Form을 사용하여 슬랙에서 보낸 데이터를 받습니다. (Pydantic 모델을 사용하지 않고, Form을 사용하여 간단하게 처리합니다.)
@app.post("/event")
async def event(
    # 슬랙에서 보낸 데이터는 Form으로 받습니다.
    text: str = Form(...),  # 슬랙에서 입력한 명령어 뒤의 텍스트 (/event ... → '...' 부분)
    user_name: str = Form(...),  # 누가 보냈는지
    channel_id: str = Form(...),  # 커맨드 입력한 채널 ID
    response_url : str = Form(...)  # 슬랙에서 응답을 보낼 URL (이 URL로 응답 메시지를 보냄)
    ):

    message = eventQueryToGTP(text)
    palyload = {
        "response_type": "in_channel",  # 메시지를 채널에 공개적으로 보냄
        "text": message.content,  # GPT가 생성한 메시지 내용
    }
    # 슬랙에 메시지를 전송합니다.
    requests.post(response_url, json=palyload)
    return PlainTextResponse("GPT가 분석하여 메시지를 슬랙에 전송합니다.", status_code=200)
    
