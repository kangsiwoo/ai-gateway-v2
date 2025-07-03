from typing import Dict
from urllib.parse import urlparse

from app.core import database

from app.queues.server_queue import ServerQueue
from app.core.exceptions import ServerRegistrationError, ServerNotFoundError

class ServerService:
    def __init__(self):
        self.servers: Dict[str, ServerQueue] = {}
        self.counter = 1

    async def load_servers_from_db(self):
        rows = await database.fetch_servers()
        for row in rows:
            server_id = row["server_id"]
            url = row["url"]
            server_queue = ServerQueue(server_id, url)
            await server_queue.start_worker()
            self.servers[server_id] = server_queue
            num = int(server_id)
            if num >= self.counter:
                self.counter = num + 1

    async def register_server(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ServerRegistrationError("Invalid server URL")

        server_id = str(self.counter)
        self.counter += 1
        server_queue = ServerQueue(server_id, url)
        # worker_task를 여기서 생성 (이제 비동기 함수니까 루프가 있음)
        await server_queue.start_worker()
        self.servers[server_id] = server_queue
        await database.add_server(server_id, url)
        return server_id


    async def remove_server(self, server_id: str):
        if server_id in self.servers:
            # 워커 태스크 중지 및 서버 제거
            self.servers[server_id].stop()
            del self.servers[server_id]
            await database.remove_server(server_id)
        else:
            raise ServerNotFoundError(f"Server {server_id} not found")

    def list_servers(self):
        # 각 서버의 상태 정보 리스트 반환
        return [
            {
                "server_id": sid,
                "url": sq.server_url,
                "busy": sq.busy,
                "queue_size": sq.queue.qsize()
            }
            for sid, sq in self.servers.items()
        ]

    def get_server(self, server_id: str) -> ServerQueue:
        return self.servers.get(server_id)

# 전역으로 서버 서비스 인스턴스 생성
server_service = ServerService()
