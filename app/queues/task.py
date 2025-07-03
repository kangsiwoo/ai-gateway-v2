import asyncio

class QueryTask:
    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt
        # 현재 이벤트 루프에 연결된 Future 생성
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()