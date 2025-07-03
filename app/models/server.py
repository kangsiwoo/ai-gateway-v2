from pydantic import BaseModel

class RegisterServerRequest(BaseModel):
    url: str         # 해당 AI 서버의 요청 URL (엔드포인트)

class ServerInfoResponse(BaseModel):
    server_id: str
    url: str
    busy: bool       # 현재 처리 중 여부
    queue_size: int  # 대기열에 남은 작업 수