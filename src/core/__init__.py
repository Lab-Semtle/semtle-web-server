"""
환경 설정
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from decouple import config
import logging
import logging.config


# .env 파일에서 환경 변수 로드
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class GeneralSettings(BaseSettings):
    DEBUG: bool = True # 로깅 레벨 설정 / True -> DEBUG 모드, False -> INFO 모드
    FERNET_KEY: str = os.getenv("FERNET_KEY")
    SEND_EMAIL_USERNAME: str = os.getenv("SEND_EMAIL_USERNAME")
    SEND_EMAIL_PASSWORD: str = os.getenv("SEND_EMAIL_PASSWORD")
    
class RDBSettings(BaseSettings):
    DB_PROTOCAL: str = "postgresql+asyncpg"  # asyncpg | psycopg 이지만 psycopg3 사용(비동기가능/벡터DB+RDB)
    DB_USERNAME: str = os.getenv("DB_USERNAME") 
    DB_PASSWORD: SecretStr = SecretStr(os.getenv("DB_PASSWORD"))  
    DB_HOST: str = os.getenv("DB_HOST") 
    DB_PORT: str = os.getenv("DB_PORT") 
    DB_NAME: str = os.getenv("DB_NAME") 
    
    @property # 메서드를 클래스 속성처럼 사용 가능
    def DATABASE_URL(self) -> str:
        return f"{self.DB_PROTOCAL}://{self.DB_USERNAME}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class JWTSettings(BaseSettings):
    JWT_SECRET_ACCESS_KEY: str = os.getenv("JWT_SECRET_ACCESS_KEY")
    JWT_SECRET_REFRESH_KEY: str = os.getenv("JWT_SECRET_REFRESH_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_MIN: float = float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: float = float(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

class Settings:
    general: GeneralSettings = GeneralSettings()    
    rdb: RDBSettings = RDBSettings()
    jwt: JWTSettings = JWTSettings()
    
settings = Settings()


"""
로깅 설정
"""
def setup_logging():
    logging.basicConfig(
        format=r"[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt= r"%m/%d/%Y %I:%M:%S %p",
        level= logging.DEBUG if settings.general.DEBUG else logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log"),
        ]
    )
    
    # 파일 헨들러는 디테일한 포맷 추가
    file_handler = logging.getLogger().handlers[-1]
    file_handler.setFormatter(logging.Formatter(
        r"[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p"
    ))
    
    _logger = logging.getLogger(__name__)
    _logger.info("환경 설정(src/core/__init__.py) 로드 완료")