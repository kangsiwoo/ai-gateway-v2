import asyncio
from datetime import datetime
from app.log import elasticsearch as es_logging
from app.core.utils import send_to_ai_server
from app.core.config import settings
from app.queues.task import QueryTask

class ServerQueue:
    def __init__(self, server_id: str, server_url: str):
        self.server_id = server_id
        self.server_url = server_url
        self.queue = asyncio.Queue()
        self.busy = False
        self._worker_task = None

    async def start_worker(self):
        self._worker_task = asyncio.create_task(self._worker_loop())

    async def _worker_loop(self):
        """큐에 있는 쿼리들을 순차 처리하는 워커 루프."""
        while True:
            task: QueryTask = await self.queue.get()      # 대기열에서 다음 작업 가져오기
            try:
                self.busy = True
                # AI 서버에 쿼리 전송 및 결과 획득
                result = await send_to_ai_server(
                    self.server_url,
                    task.model,
                    task.prompt,
                    settings.ai_api_token,
                )
                # Elasticsearch에 로그 저장
                # if es_logging.es:
                #     log_doc = {
                #         "timestamp": datetime.utcnow().isoformat(),
                #         "server_id": self.server_id,
                #         "model": task.model,
                #         "prompt": task.prompt,
                #         "result": result,
                #     }
                #     try:
                #         await es_logging.es.index(index="query_logs", document=log_doc)
                #     except Exception as e:
                #         print(f"Failed to log to ES: {e}")
                # 쿼리 Future에 결과 설정 -> 대기 중이던 요청에 결과 전달
                task.future.set_result(result)
            except Exception as e:
                task.future.set_exception(e)  # 에러 발생 시 Future 예외 설정
            finally:
                self.busy = False
                self.queue.task_done()        # 해당 작업 처리 완료 표시

    def submit_query(self, model: str, prompt: str):
        """새 쿼리를 큐에 넣고 Future를 반환한다."""
        task = QueryTask(model, prompt)
        # 비동기 큐에 작업 추가 (즉시 반환, 워커는 백그라운드에서 처리)
        self.queue.put_nowait(task)
        return task.future

    def stop(self):
        """워커 태스크를 중지시키고 큐 처리를 종료한다."""
        self._worker_task.cancel()
        # 필요하다면 추가 정리 로직 (예: 남은 queue 항목 처리) 구현