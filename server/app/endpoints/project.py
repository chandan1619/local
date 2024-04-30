
# pylint: disable=import-error
import os
import time
from typing import List, Optional

from app.db.database import session
from app.endpoints.document import create_document
from app.models.document import DocumentChunkMapping
from app.models.project import Project
from app.models.user import User
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()

class DocumentBase(BaseModel):
    id: str
    filename: str

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    id: str
    name: str
    email: Optional[str]
    documents: List[DocumentBase] = []

    class Config:
        orm_mode = True


async def upload_document_internal(file: UploadFile,project_id):
    if not file.filename:
        raise ValueError("No file was provided.")

    timestamp = int(time.time())
    new_filename = f"{timestamp}_{file.filename}"

    upload_directory = "uploads"
    os.makedirs(upload_directory, exist_ok=True)

    file_path = os.path.join(upload_directory, new_filename)
    with open(file_path, "wb") as f:
        contents = await file.read()  # Be cautious with large files
        f.write(contents)

    # create_document now participates in the outer transaction
    db_document, chunk_ids = create_document(project_id, filename=new_filename, path=file_path)
    
    try:
        for chunk_id in chunk_ids:
            db_chunk_mapping = DocumentChunkMapping(document_id=db_document.id, chunk_id=chunk_id)
            session.add(db_chunk_mapping)
            session.flush()
        # No commit here, as we want to commit outside
    except Exception as e:
        print(e)

    return {"message": "Document uploaded successfully", "filename": new_filename, "document": db_document}

@router.post('/create')
async def create_project(name: str = Form(...), user_id: str = Form(...), files: List[UploadFile] = File(...)):
    # Start a transaction
    try:
        # Use the session's begin_nested() for a nested transaction that can be rolled back independently
        # This ensures the whole block is treated as a single transaction
        # with db.begin_nested():
        project = Project(name=name, user_id=str(user_id))
        session.add(project)
        # Flush to get the project ID without committing the transaction
        session.flush()
        
        upload_results = []
        for file in files:
            # upload_document_internal now uses the same transaction
            result = await upload_document_internal(file,project.id)
            upload_results.append(result)

        
        # Commit the transaction at the end of all operations
        print("committing into db")
        session.commit()
        print("committing done")

        return {"project_id": project.id, "uploads": upload_results}
    except Exception as e:
        session.rollback()  # Roll back the transaction on any error
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    
def get_current_user_role(user_id) -> str:
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return user.role_id
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/projects", response_model=List[ProjectBase])
def read_projects(id: str, skip: int = 0, limit: int = 100):
    user_role_id = get_current_user_role(id)
    
    # Assuming role_id 1 is for admins, adjust based on your role definitions
    if user_role_id == "admin":
        projects_with_user_email = session.query(Project, User.email).join(User, Project.user_id == str(User.id)).offset(skip).limit(limit).all()
        projects = []
        for project, email in projects_with_user_email:
            projects.append(ProjectBase(
                id=project.id,
                name=project.name,
                email=email,
                documents=[DocumentBase(id=document.id, filename=document.filename) for document in project.documents]
            ))
        return projects
    else:
        projects = session.query(Project).filter(Project.user_id == str(id)).offset(skip).limit(limit).all()
        return [
            ProjectBase(
                id=project.id,
                name=project.name,
                email= None,
                documents=[DocumentBase(id=document.id, filename=document.filename) for document in project.documents]
            )
            for project in projects
        ]
