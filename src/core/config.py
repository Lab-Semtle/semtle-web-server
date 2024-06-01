import os
import logging
import logging.config
from dotenv import load_dotenv


load_dotenv()


class Settings:
    DB_PROTOCAL: str = "postgresql+asyncpg"  # 환경변수에 저장해야 함
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"

    DATABASE_URL = f"{DB_PROTOCAL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "detailed",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
