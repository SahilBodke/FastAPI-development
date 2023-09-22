# To Run: uvicorn app.main:app --reload
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from pydantic_settings import BaseSettings
from .config import settings
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware




# models.Base.metadata.create_all(bind = engine) # No longer req cuz we're using Alembic. This told sqlalchemy to generate all tables on startup

# app = FastAPI()

origins = ["*"]   # List of domains that can talk to our API

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# http url routes' order matters if url endpoint is same
@app.get("/")
def root():
    return {"message": "Hello, Successfully deployed from CI/CD pipeline to ubuntu!!"} 




