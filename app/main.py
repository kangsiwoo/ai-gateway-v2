from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import servers, queries
from app.log import elasticsearch as es_logging

app = FastAPI()

# Include routes for servers and queries endpoints
app.include_router(servers.router, prefix="/servers", tags=["servers"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])

# Startup event: initialize resources (e.g., Elasticsearch client)
@app.on_event("startup")
async def startup_event():
    # Initialize AsyncElasticsearch client using settings
    es_logging.es = es_logging.get_elasticsearch_client(
        settings.es_host,
        settings.es_api_token,
    )
    # (Optional) If there are pre-configured servers to add at startup, do it here.
    return

# Shutdown event: clean up resources
@app.on_event("shutdown")
async def shutdown_event():
    if es_logging.es:
        await es_logging.es.close()