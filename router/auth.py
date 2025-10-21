from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import oauth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import validators
import schemas
from database import get_db
from model import User
from utils.security import Hash, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=schemas.Showuser)
def register(login: schemas.User, db: Session = Depends(get_db)):
    email = db.query(User).filter(User.email == login.email).first()
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(username=login.username, email=login.email, password=Hash.argon(login.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
        "id": user.id,
        "name": user.username,
        "email": user.email
    }
    }
