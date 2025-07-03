from fastapi import APIRouter, HTTPException
from app.models.server import RegisterServerRequest, ServerInfoResponse
from app.services.server_service import server_service

router = APIRouter()

@router.post("/register", response_model=ServerInfoResponse)
async def register_server(req: RegisterServerRequest):
    try:
        server_id = await server_service.register_server(req.url)
        server = server_service.get_server(server_id)
        if server is None:
            raise HTTPException(status_code=500, detail="Server registration failed")
        return ServerInfoResponse(
            server_id=server_id,
            url=req.url,
            busy=server.busy,
            queue_size=server.queue.qsize()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}")
def remove_server(server_id: str):
    try:
        server_service.remove_server(server_id)
        return {"message": f"Server {server_id} removed"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[ServerInfoResponse])
def list_servers():
    return [
        ServerInfoResponse(
            server_id=s["server_id"],
            url=s["url"],
            busy=s["busy"],
            queue_size=s["queue_size"],
        )
        for s in server_service.list_servers()
    ]

@router.get("/{server_id}/status", response_model=ServerInfoResponse)
def server_status(server_id: str):
    server = server_service.get_server(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return ServerInfoResponse(
        server_id=server_id,
        url=server.server_url,
        busy=server.busy,
        queue_size=server.queue.qsize()
    )