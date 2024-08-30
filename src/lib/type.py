"""
API 반환 형식 정의
- API 응답 형식 일관성 유지 목적
- return 이후 ResultType(status='', message='', detail=item)
"""
from src.lib.dto import BaseDTO


class ResultType(BaseDTO):
    status: str  # 응답 상태('sussess'/ 'error')
    message: str # 응답 메세지
    detail: dict[str, str] | str = {} # 반환 형식(딕셔너리)
