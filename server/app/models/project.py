# pylint: disable=import-error
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User

if TYPE_CHECKING:
    from .document import Document




class Project(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name : Mapped[str] = mapped_column(String, index=True)
    documents : Mapped[List[Document]] = relationship("Document", back_populates="project")
    user_id : Mapped[User.id] = mapped_column(String,ForeignKey('users.id'))
    user: Mapped[User] = relationship("User",back_populates = "projects")