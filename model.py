from sqlalchemy import Integer, Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    projects = relationship('Project', back_populates='user', cascade="all, delete")
    comments = relationship('Comment', back_populates='user', cascade="all, delete")


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    tech_stack = Column(String(255))
    image = Column(String(255))
    github_link = Column(String(255))
    live_link = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='projects')
    comments = relationship('Comment', back_populates='project', cascade="all, delete")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    message = Column(Text, nullable=False)

    user = relationship('User', back_populates='comments')
    project = relationship('Project', back_populates='comments')
