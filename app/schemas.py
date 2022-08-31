from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# * #################################  USER #################################


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr # pip install email-validator (already installed when we did pip install fastapi[all])
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# * ################################# POST #################################


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int


# * ################################# TOKEN #################################


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# * ################################# VOTE #################################


class Vote(BaseModel):
    post_id: int
    dir: bool