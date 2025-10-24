from datetime import datetime, timedelta, timezone

from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from model import User

pwd_cxt = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash():
    def argon(password: str):
        return pwd_cxt.hash(password)

    def verify(password: str, hashed_password: str):
        return pwd_cxt.verify(password, hashed_password)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError as error:
        raise credentials_exception



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == verify_access_token(token, credentials_exception)).first()
    if user is None:
        raise credentials_exception
    return user

def send_password_reset(email: str, token: str):
    reset_link = f"https://localhost:8000/auth/password/reset/{token}"
    print(f"Password reset link: {reset_link} for email: {email}")