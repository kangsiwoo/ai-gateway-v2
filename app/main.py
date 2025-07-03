from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from app.core.exceptions import AppException
from app.core.config import settings
from app.api.routes import servers, queries
from app.log import elasticsearch as es_logging
from app.core import database
from app.services.server_service import server_service

app = FastAPI()

# Include routes for servers and queries endpoints
app.include_router(servers.router, prefix="/servers", tags=["servers"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    if isinstance(exc, AppException):
        return JSONResponse(status_code=500, content={"detail": str(exc)})
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Startup event: initialize resources (e.g., Elasticsearch client)
@app.on_event("startup")
async def startup_event():
    # Initialize AsyncElasticsearch client using settings
    es_logging.es = es_logging.get_elasticsearch_client(
        settings.es_host,
        settings.es_api_token,
    )
    await database.connect_db()
    await server_service.load_servers_from_db()
    return

# Shutdown event: clean up resources
@app.on_event("shutdown")
async def shutdown_event():
    if es_logging.es:
        await es_logging.es.close()
    await database.close_db()
