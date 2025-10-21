from sqlalchemy import Integer, Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    projects = relationship('Project', backref='user')


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    tech_stack = Column(String)
    image = Column(String)
    github_link = Column(String)
    live_link = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
