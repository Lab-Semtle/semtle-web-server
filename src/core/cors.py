"""
CROS 미들웨어 설정 모듈
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI):
    """ FastAPI 애플리케이션에 CORS 미들웨어를 설정 """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],    # 모든 도메인 요청 허용
        allow_methods=["*"],    # 모든 메서드 요청 허용
        allow_headers=["*"],    # 요청 시 모든 헤더 허용
        expose_headers=["*"],   # 모든 헤더 자바스크립트 접근 허용
        allow_credentials=True,  # 쿠키, 인증 헤더 요청 허용
    )
