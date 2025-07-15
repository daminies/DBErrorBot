# slack.py
# webhook 으로 결과 반환

# Slack Webhook 호출을 위한 HTTP 요청 라이브러리
import requests

# HMAC-SHA256 해시 계산에 사용
import hmac
import hashlib

# 환경 변수 관련
import os
from dotenv import load_dotenv

# .env 파일의 환경 변수들을 시스템에 등록
load_dotenv()


# Slack Webhook URL (메시지 전송+검증용)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

def send_slack(text: str):
    requests.post(SLACK_WEBHOOK_URL, json={"text": text})

def verify_slack_signature(timestamp: str, body: bytes, signature: str) -> bool:
    sig_basestring = f"v0:{timestamp}:{body.decode()}"
    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(my_signature, signature)


