# vector_db.py
# internal_data 및 vendor_data 디렉토리의 .md 문서를 벡터화하고
# FAISS 인덱스를 생성/로딩/갱신하는 기능을 담당

# 파일 경로
from pathlib import Path
# .md 파일 로드용
from langchain_community.document_loaders import TextLoader
# 문서 분할
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 문서 입베딩
from langchain_community.embeddings import HuggingFaceEmbeddings
# 벡터 DB 라이브러리
from langchain_community.vectorstores import FAISS


# 내부 문서 인덱스 경로
INDEX_PATH = Path("faiss_index")
# 벤더 문서 인덱스 경로  
VENDOR_INDEX_PATH = Path("vendor_index")
# 사전학습된 문장 임베딩 모델 사용
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_vector_db():
    # 기존 인덱스 존재 시 로딩
    if INDEX_PATH.exists():
        return FAISS.load_local(str(INDEX_PATH), embedding_model, allow_dangerous_deserialization=True) 
    # 새 인덱스 생성
    docs = []
    for file in Path("internal_data").glob("*.md"):
        loader = TextLoader(str(file), encoding="utf-8")
        docs.extend(loader.load()) # Document 객체 리스트에 추가
    # 문서 조각으로 분할 (500자 단위, 50자 중첩)
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs) 
    # FAISS 벡터 인덱스 생성
    db = FAISS.from_documents(chunks, embedding_model)
    # 인덱스 디스크에 저장
    db.save_local(INDEX_PATH)
    return db

def load_vendor_db():
    if VENDOR_INDEX_PATH.exists():
        return FAISS.load_local(str(VENDOR_INDEX_PATH), embedding_model, allow_dangerous_deserialization=True)
    vendor_docs = []
    for file in Path("vendor_data").glob("*.md"):
        loader = TextLoader(str(file), encoding="utf-8")
        vendor_docs.extend(loader.load())
    vendor_chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(vendor_docs)
    vendor_db = FAISS.from_documents(vendor_chunks, embedding_model)
    vendor_db.save_local(VENDOR_INDEX_PATH)
    return vendor_db


def update_internal_and_vendor_index(vector_db):
    new_docs = []
    for file in Path("internal_data").glob("*.md"):
        loader = TextLoader(str(file), encoding="utf-8")
        new_docs.extend(loader.load())
    # 문서 분할 (chunk_size를 몇으로 해야할지..?)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(new_docs)
    # 기존 인덱스에 문서 추가
    vector_db.add_documents(split_docs)

    # 벤더 문서도 같은 방식으로 추가
    vendor_docs = []
    for file in Path("vendor_data").glob("*.md"):
        loader = TextLoader(str(file), encoding="utf-8")
        vendor_docs.extend(loader.load())
    vendor_chunks = splitter.split_documents(vendor_docs)
    vector_db.add_documents(vendor_chunks)

    # 업데이트된 인덱스를 디스크에 저장
    vector_db.save_local(INDEX_PATH)
    return "internal_data 및 vendor_data 문서들을 인덱스에 추가했습니다."




