from fastapi import APIRouter, HTTPException, Query
from app.models.query import QueryRequest, QueryResponse
from app.services.query_service import query_service
from app.log.elasticsearch import search_logs

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def query_ai(request: QueryRequest):
    try:
        return await query_service.handle_query_request(request)
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/logs")
async def search_query_logs(q: str = Query(..., description="검색할 쿼리 문자열")):
    hits = await search_logs(q)
    return {"results": [hit["_source"] for hit in hits]}