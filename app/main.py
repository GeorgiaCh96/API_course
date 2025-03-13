from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/?h=cors#use-corsmiddleware
#if your APIs where configured for a specific Webapp, you have to provide the specific origins that can access my API

#origins = ["https://www.google.com/", "https://www.youtube.com/"]  # all domains that can talk to our API
origins = ["*"]  # all domains that can talk to our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow all methods (POST, GET ETC.)
    allow_headers=["*"],   # allow all headers
)

# Create Database tables
# models.Base.metadata.create_all(bind=engine)  # since we set up alembic, we can remove this line

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# request Get method url: "/"
@app.get("/") 
def root():
    return {"message": "Welcome to my NEW API! Pushing out to ubuntu"}
