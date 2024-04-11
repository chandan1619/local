import uuid
from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base  # Assuming .base is where your Base declarative class is defined


class DataSourceType(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    github = "github"
    slack = "slack"
    discord = "discord"
    jira = "jira"
    # Extend with more types as needed

class DataSource(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    type: Mapped[DataSourceType] = mapped_column(SQLAlchemyEnum(DataSourceType))

class UserDataSource(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "user_data_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    data_source_id: Mapped[str] = mapped_column(String, ForeignKey("data_sources.id"))
    credentials: Mapped[str] = mapped_column(String, nullable=True)  # Consider storing encrypted credentials

    # Relationship to DataSource
    data_source: Mapped[DataSource] = relationship("DataSource")
