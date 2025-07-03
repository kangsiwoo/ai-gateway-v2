from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    es_host: str = "http://localhost:9200"
    es_api_token: str = ""
    ai_api_token: str = ""
    db_url: str = os.environ.get("DB_URL")
    db_username: str = os.environ.get("DB_USERNAME")
    db_password: str = os.environ.get("DB_PASSWORD")
    # 추가 설정 가능 (예: 초기 서버 목록 등)

settings = Settings()  # 환경 변수 로드하여 설정 객체 생성