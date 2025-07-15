# routes.py

# 메시지 수신시 internal_data → vendor_data 순서로 탐색
# 결과가 부정확할시 ChatGPT에게 해결방안/원인 보완 요청  
# 결과를 Slack에 전송


# FastAPI 요청 객체를 다루기 위해 import
from fastapi import Request
from typing import List
import json
import time

# 슬랙 메시지를 처리하기 위한 데이터 구조
from app.models import errorlog

# 유틸 함수: ORA 코드 추출, 슬랙 메시지 포맷 처리
from app.utils import extract_ora_code, slackify_links, clean_md

# Slack 관련 기능: 메시지 전송, 시그니처 검증
from app.slack import send_slack, verify_slack_signature

# ERROR LOG 로 문서 검색
<<<<<<< HEAD
from app.vector_search import search_md_by_code
=======
from app.vector_search_internal import search_internal_md
from app.vector_search_vendor import search_vendor_md
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759

# DB 타입 구분 -> 현재 미사용
from app.db_error_classifier import classify_error_type

# FAISS 기반 벡터 DB 로딩 함수
from app.vector_db import load_vector_db, load_vendor_db, update_internal_and_vendor_index

# langchain 문서 객체
from langchain_core.documents import Document

# LLM 활용 최종 점검
from app.llm import run_final_llm_review


# 벡터 DB 로딩 (앱 시작 시 1회 수행)
vector_db = load_vector_db()
vendor_vector_db = load_vendor_db()


# 슬랙 메시지 중복 방지용 캐시 (timestamp 기반)
recent_ts_cache = {}



async def log_and_notify(log: errorlog):
    
     # 1. 에러 메시지에서 ORA-XXXXX 패턴이 있을 경우 추출  
    ora_code = extract_ora_code(f"{log.title} {log.content}")
    query_text = f"{log.title}\n\n{log.content}"

    matched_sample = None
    matched_vendor = None

    # 2. ORA 코드가 있을 경우: 코드 기반 검색
    if ora_code:
<<<<<<< HEAD
        matched_sample = search_md_by_code(ora_code, "internal_data")
        matched_vendor = search_md_by_code(ora_code, "vendor_data")
=======
        matched_sample = search_internal_md(ora_code)
        matched_vendor = search_vendor_md(ora_code)
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759

    # 3. 결과가 없으면 유사도 검색 수행 (벡터 DB에서 검색)
    if not matched_sample:
        results: List[Document] = vector_db.similarity_search(query_text, k=1)
        if results:
            matched_sample = clean_md(results[0].page_content)

    if not matched_vendor:
        vendor_results = vendor_vector_db.similarity_search(query_text, k=1)
        if vendor_results:
            matched_vendor = clean_md(vendor_results[0].page_content)

    # 4. 검색된 문서 조합
    sections = []
    if matched_sample:
        sections.append(f"📘 내부 문서\n{matched_sample}")
    if matched_vendor:
        sections.append(f"📕 벤더 문서\n{matched_vendor}")

    context_combined = "\n\n".join(sections)

    # 5. GPT에게 "최종 리뷰" 요청 (문서가 적절한지 평가하고 재구성)
    final_response = run_final_llm_review(query_text, context_combined)

    # 6. Slack으로 최종 분석 결과 전송
    send_slack(f"*📊 분석 결과 도착!*\n{slackify_links(final_response)}")

    return {"message": "분석 완료"}




# .md 파일 추가시 신규 index rebuild 수행
def update_index():
    msg = update_internal_and_vendor_index(vector_db)
    return {"message": msg}



# slack 메세지 수신 handler
async def slack_events(request: Request):
    # 요청 body 및 헤더 정보 추출
    body = await request.body()
    headers = request.headers
    timestamp = headers.get("X-Slack-Request-Timestamp")
    slack_signature = headers.get("X-Slack-Signature")

    # 슬랙에서 온 요청인지 확인 (보안 검증)
    if not verify_slack_signature(timestamp, body, slack_signature):
        return {"error": "Invalid signature"}

    # body 파싱
    payload = json.loads(body)

    # 슬랙 URL 검증 요청 (앱 최초 등록 시 사용)
    if payload.get("type") == "url_verification":
        return payload.get("challenge")

    # 실제 이벤트 수신 처리
    if payload.get("type") == "event_callback":
        event = payload.get("event", {})
        # 메시지 수신 이벤트일 경우 (subtype은 bot 메시지 등 필터링)
        if event.get("type") == "message" and "subtype" not in event:
            ts = event.get("ts")    # 타임스탬프 기반 중복 메시지 필터링
            text = event.get("text", "") 

            if ts in recent_ts_cache:
                return {"message": "Duplicate ignored"} 

            # 캐시에 타임스탬프 저장
            recent_ts_cache[ts] = time.time() 

            # 분석 수행
            result = await log_and_notify(errorlog(title="Slack Message", content=text)) 

            # 발송 
<<<<<<< HEAD
            send_slack(f"*분석 완료 여부 *\n{result['message']}")
=======
            send_slack(f"*분석 완료*\n{result['message']}")
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759

					   

    return {"ok": True}


<<<<<<< HEAD

=======
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759
