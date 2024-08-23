"""
HTTP 상태코드 및 메시지 커스터마이징
"""

class ER:
    """ 에러 상태 코드 및 메시지 정의 """
    INVALID_REQUEST = (400, '잘못된 요청입니다.')
    UNAUTHORIZED = (401, '인증되지 않았습니다.')
    FORBIDDEN = (403, '접근이 금지되었습니다.')
    NOT_FOUND = (404, '해당 리소스를 찾을 수 없습니다.')
    DUPLICATE_RECORD = (409, '중복된 아이디가 존재합니다.')
    FIELD_VALIDATION_ERROR = (422, '필드 유효성 검증에 실패하였습니다.')
    INTERNAL_ERROR = (500, '서버 내부에 오류가 발생했습니다.')

class SU:
    """ 성공 상태 코드 및 메시지 정의 """
    SUCCESS = (200, '요청이 성공적으로 처리되었습니다.')
    CREATED = (201, '리소스가 성공적으로 생성되었습니다.')
    ACCEPTED = (202, '요청이 접수되었습니다.')

class Status:
    """
    HTTP 응답 상태 코드와 메시지를 문서화
    - api 작성 시 responses에서 사용
    - `docs` 메서드를 사용하여 상태 코드와 설명을 반환
    """
    @staticmethod
    def docs(*status_codes):
        response_docs = {}
        for status in status_codes:
            response_docs[status[0]] = {"description": status[1]}
        return response_docs
