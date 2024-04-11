# pylint: disable=import-error
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .project import Project



class Role(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "roles"
    id : Mapped[str] = mapped_column(String, primary_key=True, index=True)
    role_name : Mapped[str] = mapped_column(String, index=True)
    user : Mapped[User] = relationship("User", back_populates = "role")


class User(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "users"

    id : Mapped[str] = mapped_column(String, primary_key=True, index=True,default=str(uuid.uuid4()))
    name : Mapped[str] = mapped_column(String)
    username : Mapped[str] = mapped_column(String,nullable=True)
    email : Mapped[str] = mapped_column(String, unique=True, index=True)
    password : Mapped[str] = mapped_column(String, nullable = True)
    projects : Mapped[List[Project]] = relationship("Project", back_populates = "user")
    role_id : Mapped[Role.id] = mapped_column(String,ForeignKey("roles.id"))
    role : Mapped[Role] = relationship("Role", back_populates = "user")
     


