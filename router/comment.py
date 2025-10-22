from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import CommentModel, CommentsModelList
from utils.security import get_current_user
from model import Comment, Project, User

router = APIRouter(
    prefix="/comment",
    tags=["comment"]

)

@router.post('create_comment/{project_id}', response_model=CommentModel)
def create_comment(project_id: int, comment: CommentModel, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing_project = db.query(Project).filter(Project.id == project_id).first()
    if not existing_project:
        raise HTTPException(status_code=404, detail="post not found")
    comment = Comment(
        project_id=project_id,
        user_id=current_user.id,
        message=comment.message,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get('/comment/{project_id}', response_model=List[CommentsModelList])
def get_comment(project_id: int,db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.project_id == project_id).all()
    if not comment:
        raise HTTPException(status_code=404, detail="post not found")
    output = [
        CommentsModelList(
            username=db.query(User).filter(User.id == comment.user_id).first().username,
            message=comment.message,
        )
    for comment in comment
    ]
    return output

@router.delete('/comment/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    db.delete(comment)
    db.commit()
    return {"msg": 'comment deleted'}
