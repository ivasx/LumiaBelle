from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel
from typing import List

class CartModel(BaseModel):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)

    user: Mapped["UserModel"] = relationship(back_populates='cart')
    items: Mapped[List["CartItemModel"]] = relationship(back_populates='cart', cascade='all, delete-orphan')