from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    password: str



class Showuser(BaseModel):
    username: str
    email: EmailStr
    class Config():
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class ProjectsModel(BaseModel):
    title: str
    description: str
    tech_stack: Optional[str] = None
    image: Optional[str] = None
    github_link: Optional[HttpUrl] = None
    live_link: Optional[HttpUrl] = None


class ProjectsModelCreate(BaseModel):
    title: str
    description: str
    tech_stack: Optional[str]
    image: Optional[str]
    github_link: Optional[str]
    live_link: Optional[str]


class ProjectsModelList(BaseModel):
    title: str
    description: str
    tech_stack: Optional[str]
    image: Optional[str]
    github_link: Optional[str]
    live_link: Optional[str]
    user: str



class CommentModel(BaseModel):
    message: str

class CommentsModelList(BaseModel):
    username: str
    message: str