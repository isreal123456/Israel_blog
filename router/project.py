from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import CommentModel
from utils.security import get_current_user
from model import Comment, Project

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