from datetime import datetime

from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel

from .utils import nowtime


class Link(SQLModel, table=True):
    __tablename__ = "links"  # type: ignore[assignment]

    id: int = Field(default=None, primary_key=True, index=True)

    original_url: str = Field(index=True, unique=True, max_length=2048, nullable=False)
    short_url: str = Field(index=True, unique=True, max_length=20, nullable=False)
    clicks: int = Field(default=0, ge=0, nullable=False)

    created_at: datetime = Field(default_factory=nowtime, nullable=False)

    expires_at: datetime | None = Field(
        default=None,
        index=True,
        nullable=True,
    )


class CreateLinkRequest(BaseModel):
    url: HttpUrl
