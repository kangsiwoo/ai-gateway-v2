from elasticsearch import AsyncElasticsearch

es = None  # 전역 Elasticsearch 클라이언트 (startup에서 초기화)

def get_elasticsearch_client(es_host: str, token: str = ""):
    """AsyncElasticsearch 클라이언트를 생성하여 반환."""
    return AsyncElasticsearch(hosts=[es_host], bearer_auth=token) if token else AsyncElasticsearch(hosts=[es_host])

async def search_logs(query_text: str):
    """저장된 쿼리 로그에서 주어진 텍스트를 검색."""
    if not es:
        raise RuntimeError("Elasticsearch client is not initialized")
    # 'query' 필드에 query_text를 매치하는 단순 검색 예시
    resp = await es.search(
        index="query_logs",
        query={"match": {"query": query_text}}
    )
    return resp.get("hits", {}).get("hits", [])