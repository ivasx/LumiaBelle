from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import BaseModel


class Color(BaseModel):
    __tablename__ = 'color'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hex_code: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)