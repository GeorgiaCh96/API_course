"""
    Create different models for each different request
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing_extensions import Annotated

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class Post(BaseModel):
    # schema / Pydantic model for 'Post'

    title: str
    content: str
    published: bool = True   # optional field for user, default value for published is True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True   # optional field for user, default value for published is True

class PostCreate(PostBase):  # all of our pydantic models must inherit from PostBase (create new models using PostBase)
    pass


# Define what data you want to return in Response
class Post(PostBase):   
    # inherit fields from PostBase class and add any extra fields you need:
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # pydantic model

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post   # refering to pdantic Post (previous class)
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Define a schema for the token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]   #conint(le=1)   # <= 1, dir gets values 0 or 1