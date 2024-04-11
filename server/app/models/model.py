# pylint: disable=import-error
import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Model(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "models"

    id : Mapped[str] = mapped_column(String, primary_key=True, index=True,default=str(uuid.uuid4()))
    name : Mapped[str] = mapped_column(String, unique=True, index=True)
    parameters: Mapped[str] = mapped_column(String,index=True)
    ram_size: Mapped[str] = mapped_column(String,index=True)
    model_size: Mapped[str] = mapped_column(String)
    hugging_face_url : Mapped[str] = mapped_column(String)
    is_downloaded : Mapped[str] = mapped_column(Boolean,default= False)
    install_command: Mapped[str] = mapped_column(String)
    