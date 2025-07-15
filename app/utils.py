# utils.py
# DB 에러 문자열에서 ORA 코드를 추출하고
# Slack 메시지 형식에 맞게 링크/마크다운을 변환하는 유틸리티 함수들 정의
<<<<<<< HEAD

=======
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759

import re

def extract_ora_code(text: str) -> str:
    match = re.search(r"ORA-\d{5}", text)
    return match.group() if match else ""

def slackify_links(text: str) -> str:
    return re.sub(r'(https?://[^\s)]+)', r'<\1|\1>', text)

def clean_md(text: str) -> str:
    return text.replace("##", "▶")


