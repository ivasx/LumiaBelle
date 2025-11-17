from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel


class Size(BaseModel):
    __tablename__ = 'size'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
