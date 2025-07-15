# main.py 
# FastAPI 애플리케이션 초기화 및 라우트 등록

from fastapi import FastAPI, Request
from app.models import errorlog
from app.routes import log_and_notify, update_index, slack_events

app = FastAPI()

# 에러 로그 처리 엔드포인트
app.post("/log_and_notify")(log_and_notify)

# 인덱스 수동 업데이트 엔드포인트
app.post("/update_index")(update_index)

# Slack 이벤트 수신 핸들러
app.post("/slack/events")(slack_events)




