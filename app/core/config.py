from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    es_host: str = "http://localhost:9200"
    ai_api_token: str = os.environ.get('OPEN_WEB_UI_TOKEN')

settings = Settings()