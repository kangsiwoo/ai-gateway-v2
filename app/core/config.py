import os

from pydantic_settings import BaseSettings

os.environ.get()

class Settings(BaseSettings):
    es_host: str = "http://localhost:9200"
    ai_api_token: str = ""
    # 추가 설정 가능 (예: 초기 서버 목록 등)

settings = Settings()  # 환경 변수 로드하여 설정 객체 생성