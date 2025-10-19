from fastapi import FastAPI
from router import  post
import model
from database import engine

app = FastAPI()


model.Base.metadata.create_all(engine)
app.include_router(post.router)
