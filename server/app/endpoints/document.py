"""_summary_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
"""
#  pylint: disable=import-error
import os
import time
from uuid import UUID

from app.db.database import session
from app.models.document import Document, DocumentChunkMapping
from app.models.llm import upload_embeddind
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from pymilvus import Collection
from sqlalchemy.orm import Session

router = APIRouter()



def create_document(project_id, filename: str, path: str):
    try:
        db_document = Document(filename=filename, path=path, project_id=project_id)
        session.add(db_document)
        session.flush()  # Use flush here to ensure the document ID is available without committing

        # Call upload_embedding and potentially raise an exception if it fails
        chunk_ids = upload_embeddind(path, f"project{project_id}")
        
        # If upload_embedding succeeds, associate chunks with the document
        
        # Return early before committing; let the outer function handle the commit
        return db_document, chunk_ids
    except Exception as e:
        # Explicit rollback is not necessary here if using db.begin_nested() in the caller
        # but ensure the exception is propagated up
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed during document creation or embedding upload.") from e

@router.post("/upload/", responses={
    200: {
        "description": "Document uploaded successfully",
        "content": {
            "application/json": {
                "example": {"message": "Document uploaded successfully", 
                            "filename": "12345678_example.pdf"}
            }
        },
    },
    400: {
        "description": "Invalid file or bad request",
    },
})
async def upload_document(file: UploadFile,project_id: UUID):
    """_summary_

    Args:
        file (UploadFile): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:db
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # Ensure that a file is provided
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file was provided.")

    # Prepend the current timestamp to the filename to ensure uniqueness
    timestamp = int(time.time())
    new_filename = f"{timestamp}_{file.filename}"
    
    # Ensure the uploads directory exists
    upload_directory = "uploads"
    os.makedirs(upload_directory, exist_ok=True)

    try:
        # Save the uploaded file to a local folder with the new filename
        file_path = f"{upload_directory}/{new_filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        # Handle unexpected errors when saving the file
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, \
                            detail="Could not save the file.") from e

    try:
        # Create a new document record in the database
        db_document, chunk_ids = create_document(project_id, filename=new_filename, path=file_path)

        for chunk_id in chunk_ids:
            db_chunk_mapping = DocumentChunkMapping(document_id=db_document.id, chunk_id=chunk_id)
            session.add(db_chunk_mapping)
        session.commit()  

    except Exception as e:
        # Handle unexpected errors when creating the database record
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, \
                            detail="Could not create a database record for the file.") from e
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Document uploaded successfully", "filename": new_filename, "document": db_document},
    )


@router.delete("/documents/{document_id}", responses={
    200: {
        "description": "Document and its chunks deleted successfully",
    },
    404: {
        "description": "Document not found",
    },
})


async def delete_document(document_id: int):
    """_summary_

    Args:
        document_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # Fetch the document with the given ID
    db_document = session.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    try:
        # Delete the associated chunk mappings first
        chunk_mappings = session.query(DocumentChunkMapping).filter(DocumentChunkMapping.document_id == document_id).all()
        deleted_chunk_ids = [str(mapping.chunk_id) for mapping in chunk_mappings]

        
        collection = Collection("project1")      # Get an existing collection.
        collection.delete(f"id in {list(deleted_chunk_ids)}")


        session.query(DocumentChunkMapping)\
        .filter(DocumentChunkMapping.document_id == document_id)\
        .delete(synchronize_session='fetch')
        # Now delete the document itself
        session.delete(db_document)
        # Commit the changes to the database
        session.commit()
    except Exception as e:
        # If something goes wrong, rollback the session and raise an HTTPException
        session.rollback()
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, \
                            detail="Could not delete the document and its chunks.") from e
    return {"message": "Document and its chunks deleted successfully"}


@router.get("/documents/{document_id}")
async def read_document(document_id: str):
    document = session.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = document.path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(path=file_path)