# from typing import List, Optional
# from src.api.v1.admin_user import admin_user_dao
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.api.v1.admin_user.admin_user_dto import (
#     ReadUserInfo,
#     ReadFilterUser,
# )


# async def get_filtered_users(query: Optional[str], filter: ReadFilterUser, db: AsyncSession) -> List[ReadUserInfo]:
#     ''' 승인된 유저 정보를 조건에 따라 필터링하여 가져오는 함수 '''
#     users_info = []
    
#     if filter.role and filter.grade and query:
#         # 모든 조건이 있을 때
#         role_users = await admin_user_dao.get_filter_users_by_role(filter.role, db)
#         grade_users = await admin_user_dao.get_filter_users_by_grade(filter.grade, db)
#         query_users = await admin_user_dao.get_search_users(query, db)
#         users_info = [user for user in role_users if user in grade_users and user in query_users]
#     elif filter.role and filter.grade:
#         # 역할과 등급 조건이 있을 때
#         role_users = await admin_user_dao.get_filter_users_by_role(filter.role, db)
#         grade_users = await admin_user_dao.get_filter_users_by_grade(filter.grade, db)
#         users_info = [user for user in role_users if user in grade_users]
#     elif filter.role and query:
#         # 역할과 검색어 조건이 있을 때
#         role_users = await admin_user_dao.get_filter_users_by_role(filter.role, db)
#         query_users = await admin_user_dao.get_search_users(query, db)
#         users_info = [user for user in role_users if user in query_users]
#     elif filter.grade and query:
#         # 등급과 검색어 조건이 있을 때
#         grade_users = await admin_user_dao.get_filter_users_by_grade(filter.grade, db)
#         query_users = await admin_user_dao.get_search_users(query, db)
#         users_info = [user for user in grade_users if user in query_users]
#     elif filter.role:
#         # 역할 조건만 있을 때
#         users_info = await admin_user_dao.get_filter_users_by_role(filter.role, db)
#     elif filter.grade:
#         # 등급 조건만 있을 때
#         users_info = await admin_user_dao.get_filter_users_by_grade(filter.grade, db)
#     elif query:
#         # 검색어 조건만 있을 때
#         users_info = await admin_user_dao.get_search_users(query, db)
#     else:
#         # 모든 조건이 없을 때 전체 유저 조회
#         users_info = await admin_user_dao.get_all_users(db)
    
#     return users_info


# async def get_new_users(db: AsyncSession) -> List[ReadUserInfo]:
#     ''' 회원가입 신청 완료, 미승인 유저 정보를 가져오는 함수 '''
#     users_info = await admin_user_dao.get_new_users(db)
#     return users_info


# async def update_user_activate(user_email: List[str], activate: bool, db: AsyncSession) -> None:
#     ''' 선택된 유저 계정을 활성화/비활성화하는 함수 '''
#     await admin_user_dao.update_user_activate(user_email, activate, db)


# async def update_user_role(user_email: List[str], role: str, db: AsyncSession) -> None:
#     ''' 선택된 유저 권한을 변경하는 함수 '''
#     await admin_user_dao.update_user_role(user_email, role, db)
    
    
# async def update_user_grade(user_email: List[str], grade: str, db: AsyncSession) -> None:
#     ''' 선택된 유저 등급을 변경하는 함수 '''
#     await admin_user_dao.update_user_grade(user_email, grade, db)
