from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .project import Project


class Document(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "documents"

    id : Mapped[str] = mapped_column(primary_key=True, nullable=False, default=str(uuid.uuid4()))
    filename : Mapped[str] = mapped_column(nullable=False, unique=True)
    path : Mapped[str] = mapped_column(unique=True, nullable=False)
    project_id: Mapped[Project.id] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="documents")

class DocumentChunkMapping(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'document_chunk_mapping'
    document_id : Mapped[str] = mapped_column(String, ForeignKey('documents.id'), primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String, primary_key=True)
    # Add additional fields if necessary
