from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    # Define the post's schema (a pydantic model) i.e. defines structure of request & response
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_model = True

class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut   # Return a pydantic model - User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # Vote direction. Either 0 or 1 signifying 'Like' or 'Unlike'