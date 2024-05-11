"""
사용자 정의 HTTP 응답 코드 및 메시지를 정의
"""


class ER:
    """응답 에러 코드 및 메시지 정의"""
    INVALID_REQUEST = (400, '잘못된 요청입니다.')
    NOT_FOUND = (404, '해당 리소스를 찾을 수 없습니다.')
    UNAUTHORIZED = (401, '인증되지 않았습니다.')
    FORBIDDEN = (403, '접근이 금지되었습니다.')
    DUPLICATE_RECORD = (409, '중복된 아이디가 존재합니다.')
    INTERNAL_ERROR = (500, '서버 내부에 오류가 발생했습니다.')


class SU:
    """성공 응답 코드 및 메시지 정의"""
    SUCCESS = (200, '요청이 성공적으로 처리되었습니다.')
    CREATED = (201, '리소스가 성공적으로 생성되었습니다.')
    ACCEPTED = (202, '요청이 접수되었습니다.')


class Status:
    @staticmethod
    def docs(*modes):
        rv = {}
        for mode in modes:
            rv[mode[0]] = {"description": mode[1]}
        return rv
