from src.api.v1.timetable import timetable_dao

"""
시간표 데이터 저장 함수
"""
async def post_time_data(user_email: str, data: str) -> bool:
    res = await timetable_dao.post_time_data(user_email, data)
    return res

"""
시간표 데이터 가져오기 함수
"""
async def get_time_data(user_email: str) -> None:
    result = await timetable_dao.get_time_data(user_email)
    return result