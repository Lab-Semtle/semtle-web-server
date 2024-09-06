import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from src.api.v1.comment_exam.comm_exam_ctl import router  # 프로젝트 구조에 맞게 경로를 조정하세요

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_get_exam_sharing_board_comment():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/exam_sharing_board_comment/get?exam_sharing_board_no=6&page=0")
    assert response.status_code == 200
    assert 'total' in response.json()
    assert 'Board_info' in response.json()


@pytest.mark.asyncio
async def test_create_exam_sharing_board_comment():
    payload = {
        "Content": "New Comment",
    }
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/exam_sharing_board_comment/?exam_sharing_board_no=6", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_update_exam_sharing_board_comment():
    payload = {
        "Content": "Updated Comment",
    }
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.put("/exam_sharing_board_comment/?exam_sharing_board_no=6&exam_sharing_board_comment_no=7", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_delete_exam_sharing_board_comment():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.delete("/exam_sharing_board_comment/?exam_sharing_board_no=6&exam_sharing_board_comment_no=6")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
