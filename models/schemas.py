from pydantic import BaseModel
from typing import List, Optional


class Blog(BaseModel):
    title: str
    body: str


class OrmBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserBase):
    blogs: List[OrmBlog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserBase

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
