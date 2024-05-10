from sqlalchemy.orm import Session
from src.var.session import get_db

from fastapi import APIRouter, Depends, UploadFile

from src.api.v1.post import post_dto, post_service

app = APIRouter(
    prefix = "/src/api/v1/post",
)

@app.post(path = "/create", description="기본 게시판 - 게시글 생성")
async def create_new_post(new_post: post_dto.Newpost, db: Session = Depends(get_db)):
    return post_service.insert_post(new_post, db)

@app.get(path = "/read", description="기본 게시판 - 게시글 조회")
async def read_all_post(db: Session = Depends(get_db)):
    return post_service.list_all_post(db)

@app.get(path = "/read/{post_no}", description="기본 게시판 - 특정 게시글 조회", response_model=post_dto.Post)
async def read_post(post_no: int, db: Session = Depends(get_db)):
    return post_service.get_post(post_no, db)

@app.get(path = "/read_tags/{tags}", description="기본 게시판 - 특정  태그 게시글 조회", response_model=post_dto.Post)
async def read_tags_post(tags: str, db: Session = Depends(get_db)):
    return post_service.get_tags_post(tags, db)

@app.put(path = "/update/{post_no}", description="기본 게시판 - 특정 게시글 수정")
async def update_post(update_post: post_dto.Updatepost, db: Session = Depends(get_db)):
    return post_service.update_post(update_post, db)

@app.patch(path = "/hide/{post_no}", description="기본 게시판 - 특정 게시글 숨김")
async def hide_post(post_no: int, db: Session = Depends(get_db)):
    return post_service.hide_post(post_no, db)

@app.patch(path = "/show/{post_no}", description="기본 게시판 - 특정 게시글 다시 보이기")
async def show_post(post_no: int, db: Session = Depends(get_db)):
    return post_service.show_post(post_no, db)

@app.delete(path = "/delete/{post_no}", description="기본 게시판 - 특정 게시글 영구 삭제")
async def delete_post(post_no: int, db: Session = Depends(get_db)):
    return post_service.delete_post(post_no, db)

@app.post(path = "/upload/", description="기본 게시판 - 파일 업로드")
async def upload_file(file: UploadFile):
    return post_service.upload_file(file)

@app.get(path = "/files/{file_id}", description="기본 게시판 - 특정 파일 찾기")
async def get_file_metadata(file_id: int):
    return post_service.get_file(file_id)

@app.get(path = "/download/{file_id}", description="기본 게시판 - 특정 파일 다운로드")
async def download_file(file_id: int):
    return post_service.download_file(file_id)

@app.delete("/delete_file/{file_id}", description="기본 게시판 - 특정 파일 제거")
async def delete_file(file_id: int):
    return post_service.delete_file(file_id)

@app.get("/like/{post_no}", description="기본 게시판 - 좋아요")
async def like_count(post_no: int, db: Session = Depends(get_db)):
    return post_service.like_count(post_no, db)

@app.get("/dislike/{post_no}", description="기본 게시판 - 싫어요")
async def dislike_count(post_no: int, db: Session = Depends(get_db)):
    return post_service.dislike_count(post_no, db)

@app.put(path = "/insert_comment/{post_no}", description="기본 게시판 - 특정 게시글에 댓글 추가")
async def insert_comment(comment: post_dto.Comment, db: Session = Depends(get_db)):
    return post_service.insert_comment(comment, db)

@app.get("/get_all_comment/{post_no}", description="기본 게시판 - 특정 게시글의 모든 댓글 불러오기")
async def get_all_comment(post_no: int, db: Session = Depends(get_db)):
    return post_service.get_all_comment(post_no, db)

@app.get("/get_comment/{post_no}/{comment_no}", description="기본 게시판 - 특정 게시글의 특정 댓글 불러오기")
async def get_comment(post_no: int,comment_no: int ,db: Session = Depends(get_db)):
    return post_service.get_comment(post_no, comment_no, db)

@app.delete(path = "/delete_comment/{post_no}/{comment_no}", description="기본 게시판 - 특정 게시글의 특정 댓글 삭제")
async def delete_comment(post_no: int,comment_no: int ,db: Session = Depends(get_db)):
    return post_service.delete_comment(post_no, comment_no, db)
