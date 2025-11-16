from typing import Optional

from sqlalchemy import Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

from ..products.ProductVariant import ProductVariant
from ..products.Category import Category

class Product(BaseModel):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text,
                                                       nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)


    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=False
    )




    category: Mapped["Category"] = relationship(back_populates="products")

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )
