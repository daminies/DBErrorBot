# 지정된 폴더에서 ORA 코드를 포함하는 .md 파일을 검색하고 내용을 반환
# Args:
#        ora_code (str): ORA-00000 형태의 에러 코드
#        folder (str): 검색 대상 폴더 경로 (예: "internal_data", "vendor_data")


from pathlib import Path
from app.utils import clean_md

def search_md_by_code(ora_code: str, folder: str) -> str | None:
    for file in Path(folder).glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            if ora_code in content:
                return clean_md(content)
    return None



