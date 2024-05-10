import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_PROTOCAL: str = "postgresql"  # 환경변수에 저장해야 함 +asyncpg
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"

    DATABASE_URL = f"{DB_PROTOCAL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
