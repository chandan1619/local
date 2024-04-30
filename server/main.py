# pylint: disable=import-error
import os

import uvicorn
from app.db.database import engine
from app.endpoints.auth.github_auth import router as github_auth_router
from app.endpoints.auth.jira_auth import router as jira_auth_router
from app.endpoints.auth.slack_auth import router as slack_auth_router
from app.endpoints.chat import router as chat_router
from app.endpoints.document import router as document_router
from app.endpoints.google_auth import router as auth_router
from app.endpoints.model import router as models_router
from app.endpoints.project import router as project_router
from app.endpoints.pull_data import router as pulldata_router
from app.models.base import Base
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.dialects.postgresql.base import PGDialect
from starlette.middleware.sessions import SessionMiddleware

PGDialect._get_server_version_info = lambda *args: (9, 2)

load_dotenv()
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key= os.getenv("SECRET_KEY"))
origins = [
    "https://localhost:3000",  # React development server
    "http://localhost:3000",  # React development server
    "http://localhost:8000",  # FastAPI server (if you have a frontend served by the same server)
    # Add other origins as needed
    "https://local-client.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in cross-site HTTP requests
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


print("database connected")


# app.include_router(user_router, prefix="/users")
app.include_router(chat_router, prefix="/chat")
app.include_router(document_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(models_router)
app.include_router(slack_auth_router)
app.include_router(github_auth_router)
app.include_router(pulldata_router)
app.include_router(jira_auth_router)



Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)
