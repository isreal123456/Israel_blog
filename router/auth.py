from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import oauth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import validators
import schemas
from database import get_db
from model import User
from utils.security import Hash, create_access_token, get_current_user, send_password_reset, verify_access_token
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

@router.put('/change-password')
def change_password(
        request: schemas.ChangePassword,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(request.old_password, user.password):
        return HTTPException(status_code=400, detail="Incorrect password")
    if request.new_password != request.confirm_password:
        return HTTPException(status_code=400, detail="Passwords don't match")
    user.password = Hash.argon(request.new_password)
    db.commit()
    return {"msg": "Password changed successfully"}


@router.post('/forgot-password')
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_access_token(user.email)
    send_password_reset(email=user.email, token=token)
    return {"msg": "Password reset link sent to your email"}

@router.post('/reset-password')
def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    email = verify_access_token(token=request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = Hash.argon(request.new_password)
    db.commit()
    return {"msg": "Password changed successfully"}
