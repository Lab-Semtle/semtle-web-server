from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.var.models import Board
from src.api.v1.post.post_dto import Newpost, PostList, Post, Updatepost, FileMetadata, Comment

from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse

import os
import sqlite3

def insert_post(new_post: Newpost, db: Session):
    post = Board(
        writer = new_post.writer,
        title = new_post.title,
        tags = new_post.tags,
        content = new_post.content
    )
    db.add(post)
    db.commit()

    return post.no

def list_all_post(db: Session):
    lists = db.query(Board).filter(Board.del_yn == "Y").all()
    return [PostList(no = row.no, writer = row.writer, title = row.title,tags = row.tags, date = row.date) for row in lists]

def get_post(post_no: int, db: Session):
    try:
        post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
        return Post(no = post.no, like = post.like, dislike = post.dislike, writer = post.writer, title = post.title,tags = post.tags, content = post.content, date = post.date)
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def get_tags_post(tags: str, db: Session):
    try:
        post = db.query(Board).filter(and_(Board.tags == tags, Board.del_yn == "Y")).first()
        return Post(no = post.no, like = post.like, dislike = post.dislike, writer = post.writer, title = post.title,tags = post.tags, content = post.content, date = post.date)
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def update_post(update_post: Updatepost, db: Session):
    post = db.query(Board).filter(and_(Board.no == update_post.no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        
        post.title = update_post.title
        post.content = update_post.content
        db.commit()
        db.refresh(post)
        return get_post(post.no, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def hide_post(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        post.del_yn = "N"
        db.commit()
        db.refresh(post)
        return {'msg': '숨김처리가 완료되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def show_post(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "N")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 숨김처리된 게시글 번호입니다.")
        post.del_yn = "Y"
        db.commit()
        db.refresh(post)
        return {'msg': '다시보이기가 완료되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def delete_post(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        db.delete(post)
        db.commit()
        return {'msg': '영구삭제가 완료되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

conn = sqlite3.connect("fastapi.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS files (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       filename TEXT,
       filepath TEXT
    )"""
)
conn.commit()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        cursor.execute("INSERT INTO files (filename, filepath) VALUES (?, ?)", (filename, file_path))
        conn.commit()

        return {"filename": filename, "filepath": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_file(file_id: int):
    try:
        cursor.execute("SELECT filename, filepath FROM files WHERE id=?", (file_id,))
        result = cursor.fetchone()
        if result:
            filename, filepath = result
            return FileMetadata(filename=filename, filepath=filepath)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_file(file_id: int):
    try:
        cursor.execute("SELECT filepath FROM files WHERE id=?", (file_id,))
        result = cursor.fetchone()
        if result:
            filepath = result[0]
            return FileResponse(filepath, media_type="application/octet-stream")
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_file(file_id: int):
    try:
        cursor.execute("SELECT filepath FROM files WHERE id=?", (file_id,))
        result = cursor.fetchone()
        if result:
            filepath = result[0]
            os.remove(filepath)
            cursor.execute("DELETE FROM files WHERE id=?", (file_id,))
            conn.commit()
            return {"message": "File deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def like_count(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        post.like += 1
        db.commit()
        db.refresh(post)
        return {'msg': f'좋아요 갯수: {post.like}'}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def dislike_count(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        post.dislike += 1
        db.commit()
        db.refresh(post)
        return {'msg': f'싫어요 갯수: {post.dislike}'}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def insert_comment(comment: Comment, db: Session):
    post = db.query(Board).filter(and_(Board.no == comment.no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        post.comment = f'{post.comment} {comment.comment}'
        db.commit()
        db.refresh(post)
        C = post.comment.split(' ')
        if '' in C:
            C.remove('')
        post.comment = ' '.join(C)
        db.commit()
        db.refresh(post)
        return {'msg': f'댓글 {comment.comment} 추가완료',
                '댓글': C
                }
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def get_all_comment(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        C = post.comment.split(' ')
        return {f'{post_no}번째 게시물의 모든댓글': C}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def get_comment(post_no: int, comment_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        C = post.comment.split(' ')
        C = C[comment_no]
        return {f'{comment_no}번째 댓글': C}
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')

def delete_comment(post_no: int, comment_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는게시글 번호입니다.")
        C = post.comment.split(' ')
        C.remove(C[comment_no])
        post.comment = ' '.join(C)
        db.commit()
        db.refresh(post)
        return {'msg': "댓글 제거완료",
                '댓글': C
                }
    except Exception as e:
        raise HTTPException(status_code=404, detail = f'에러({e})')