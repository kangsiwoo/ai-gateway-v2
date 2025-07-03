import asyncio
from app.models.query import QueryRequest, QueryResponse, QueryResult
from app.services.server_service import server_service

class QueryService:
    async def handle_query_request(self, request: QueryRequest) -> QueryResponse:
        futures = []
        # 요청에 담긴 각 쿼리에 대해
        for q in request.queries:
            # 대상 서버의 큐를 조회
            server_queue = server_service.get_server(q.server_id)
            if not server_queue:
                # 대상 서버가 없으면 404 오류 처리
                raise RuntimeError(f"Server {q.server_id} not found")
            # 큐에 작업 등록하고 Future 확보
            future = server_queue.submit_query(q.model, q.prompt)
            futures.append(future)
        # 모든 쿼리 Future들이 완료될 때까지 비동기 대기
        results = await asyncio.gather(*futures)
        # Future 결과들을 QueryResult 모델로 변환하여 응답 생성
        result_models = [
            QueryResult(server_id=req.server_id, result=res)
            for req, res in zip(request.queries, results)
        ]
        return QueryResponse(results=result_models)

# 전역 QueryService 인스턴스
query_service = QueryService()