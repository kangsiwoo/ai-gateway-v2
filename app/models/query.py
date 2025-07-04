from pydantic import BaseModel
from typing import List, Any

class SingleQuery(BaseModel):
    server_id: str   # 대상 AI 서버 식별자
    model: str       # 사용할 모델 이름
    prompt: str      # 질의 내용

class QueryRequest(BaseModel):
    queries: List[SingleQuery]  # 쿼리 목록 (2개 이상일 수 있음)

class QueryResult(BaseModel):
    server_id: str   # 쿼리를 보낸 서버 ID
    result: Any      # 해당 서버의 응답 결과

class QueryResponse(BaseModel):
    results: List[QueryResult]  # 모든 쿼리 결과 목록