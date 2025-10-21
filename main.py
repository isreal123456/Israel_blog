from fastapi import FastAPI


from router import  post,auth,project
import model
from database import engine

app = FastAPI()


model.Base.metadata.create_all(engine)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(project.router)