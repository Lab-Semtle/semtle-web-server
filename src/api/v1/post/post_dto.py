from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Newpost(BaseModel):
    writer: str
    title: str
    tags: Optional[str] = None
    content: Optional[str] = None

class PostList(BaseModel):
    no: int
    writer: str
    title: str
    tags: Optional[str] = None
    date: datetime

class Post(BaseModel):
    no: int
    like: int
    dislike: int
    writer: str
    title: str
    tags: Optional[str] = None
    content: Optional[str] = None
    date: datetime

class Updatepost(BaseModel):
    no: int
    title: str
    tags: Optional[str] = None
    content: Optional[str] = None

class FileMetadata(BaseModel):
    filename: str
    filepath: str

class Comment(BaseModel):
    no: int
    comment: str