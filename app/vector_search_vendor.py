
from pathlib import Path
from app.utils import clean_md

def search_vendor_md(ora_code: str) -> str:
    # vendor_data 폴더 내의 모든 .md 파일을 검색
    for file in Path("vendor_data").glob("*.md"):
        # 파일 내용을 UTF-8로 읽어오기
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            # ORA 코드가 문서 내용에 포함되어 있다면 반환 
            if ora_code in content:
                return clean_md(content)
    return None



