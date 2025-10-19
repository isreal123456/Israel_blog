from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional
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
