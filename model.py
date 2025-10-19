from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base




class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    tech_stack = Column(String)
    image = Column(String)
    github_link = Column(String)
    live_link = Column(String)


class CommentModel(BaseModel):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
