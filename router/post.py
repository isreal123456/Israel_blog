from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas, validators
from database import get_db
from model import Project

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

@router.post('/create', response_model=schemas.ProjectsModel )
def create_post(request: schemas.ProjectsModelCreate, db : Session = Depends(get_db), ):
    if not validators.url(request.github_link):
        raise HTTPException(status_code=400, detail="Github link is invalid" )
    if not validators.url(request.live_link):
        raise HTTPException(status_code=400, detail="Live link is invalid" )

    new_post = Project(
    title= request.title,
    description= request.description,
    tech_stack= request.tech_stack,
    image= request.image,
    github_link= request.github_link ,
    live_link= request.live_link,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get('/blog/{id}', response_model=schemas.ProjectsModelCreate )
def show_post(id: int, db : Session = Depends(get_db)):
    post = db.query(Project).filter(Project.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@router.get('/blog' )
def posts(db : Session = Depends(get_db)):
    posts = db.query(Project).all()
    if not posts:
        raise HTTPException(status_code=404, detail="posts not found")
    return posts

@router.put('/update/{id}', response_model=schemas.ProjectsModel )
def update_blog(id: int, request: schemas.ProjectsModelCreate, db : Session = Depends(get_db)):
    post = db.query(Project).filter(Project.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if not validators.url(request.github_link):
        raise HTTPException(status_code=400, detail="Github link is invalid" )
    if not validators.url(request.live_link):
        raise HTTPException(status_code=400, detail="Live link is invalid" )
    for key, value in request.dict(exclude_unset=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

@router.delete('/delete/{id}')
def delete_post(id: int, db : Session = Depends(get_db)):
    post = db.query(Project).filter(Project.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    db.delete(post)
    db.commit()
    return {"msg": f" deleted successfully."}

