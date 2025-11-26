from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from faker import Faker

from app.core.models import BaseModel
from app.main import app
from app.core.settings.db import db

# Import factories
from tests.users.factories import UserFactory, UserAddressFactory, CartFactory
from tests.products.factories import (
    CategoryFactory, SizeFactory, ColorFactory,
    ProductFactory, ProductVariantFactory
)
from tests.orders.factories import OrderFactory, OrderItemFactory, CartItemFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def clear_db(db_session: AsyncSession):
    for table in reversed(BaseModel.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()


@pytest_asyncio.fixture()
async def client(db_session, monkeypatch) -> AsyncGenerator[AsyncClient, Any]:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[db.get_session] = override_get_session

    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client


# Factory fixtures for Users
@pytest_asyncio.fixture
async def user_factory(db_session):
    async def _create_user(**kwargs):
        UserFactory._meta.sqlalchemy_session = db_session
        user = UserFactory.build(**kwargs)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    return _create_user


@pytest_asyncio.fixture
async def user_address_factory(db_session, user_factory):
    async def _create_address(**kwargs):
        if 'user' not in kwargs:
            kwargs['user'] = await user_factory()
        else:
            # Якщо user переданий, переконаємось що він в тій же сесії
            user = kwargs['user']
            await db_session.merge(user)

        UserAddressFactory._meta.sqlalchemy_session = db_session
        address = UserAddressFactory.build(**kwargs)
        db_session.add(address)
        await db_session.commit()
        await db_session.refresh(address)
        return address

    return _create_address


@pytest_asyncio.fixture
async def cart_factory(db_session, user_factory):
    async def _create_cart(**kwargs):
        if 'user' not in kwargs:
            kwargs['user'] = await user_factory()
        else:
            user = kwargs['user']
            await db_session.merge(user)

        CartFactory._meta.sqlalchemy_session = db_session
        cart = CartFactory.build(**kwargs)
        db_session.add(cart)
        await db_session.commit()
        await db_session.refresh(cart)
        return cart

    return _create_cart


# Factory fixtures for Products
@pytest_asyncio.fixture
async def category_factory(db_session):
    async def _create_category(**kwargs):
        CategoryFactory._meta.sqlalchemy_session = db_session
        category = CategoryFactory.build(**kwargs)
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        return category

    return _create_category


@pytest_asyncio.fixture
async def size_factory(db_session):
    async def _create_size(**kwargs):
        SizeFactory._meta.sqlalchemy_session = db_session
        size = SizeFactory.build(**kwargs)
        db_session.add(size)
        await db_session.commit()
        await db_session.refresh(size)
        return size

    return _create_size


@pytest_asyncio.fixture
async def color_factory(db_session):
    async def _create_color(**kwargs):
        ColorFactory._meta.sqlalchemy_session = db_session
        color = ColorFactory.build(**kwargs)
        db_session.add(color)
        await db_session.commit()
        await db_session.refresh(color)
        return color

    return _create_color


@pytest_asyncio.fixture
async def product_factory(db_session, category_factory):
    async def _create_product(**kwargs):
        if 'category' not in kwargs:
            kwargs['category'] = await category_factory()
        else:
            category = kwargs['category']
            await db_session.merge(category)

        ProductFactory._meta.sqlalchemy_session = db_session
        product = ProductFactory.build(**kwargs)
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product

    return _create_product


@pytest_asyncio.fixture
async def product_variant_factory(db_session, product_factory, size_factory, color_factory):
    async def _create_variant(**kwargs):
        if 'product' not in kwargs:
            kwargs['product'] = await product_factory()
        else:
            product = kwargs['product']
            await db_session.merge(product)

        if 'size' not in kwargs:
            kwargs['size'] = await size_factory()
        else:
            size = kwargs['size']
            await db_session.merge(size)

        if 'color' not in kwargs:
            kwargs['color'] = await color_factory()
        else:
            color = kwargs['color']
            await db_session.merge(color)

        ProductVariantFactory._meta.sqlalchemy_session = db_session
        variant = ProductVariantFactory.build(**kwargs)
        db_session.add(variant)
        await db_session.commit()
        await db_session.refresh(variant)
        return variant

    return _create_variant


# Factory fixtures for Orders
@pytest_asyncio.fixture
async def order_factory(db_session, user_factory, user_address_factory):
    async def _create_order(**kwargs):
        if 'user' not in kwargs:
            user = await user_factory()
            kwargs['user'] = user
        else:
            user = kwargs['user']
            await db_session.merge(user)

        if 'address' not in kwargs:
            kwargs['address'] = await user_address_factory(user=kwargs['user'])
        else:
            address = kwargs['address']
            await db_session.merge(address)

        OrderFactory._meta.sqlalchemy_session = db_session
        order = OrderFactory.build(**kwargs)
        db_session.add(order)
        await db_session.commit()
        await db_session.refresh(order)
        return order

    return _create_order


@pytest_asyncio.fixture
async def order_item_factory(db_session, order_factory, product_variant_factory):
    async def _create_order_item(**kwargs):
        if 'order' not in kwargs:
            kwargs['order'] = await order_factory()
        else:
            order = kwargs['order']
            await db_session.merge(order)

        if 'product_variant' not in kwargs:
            kwargs['product_variant'] = await product_variant_factory()
        else:
            variant = kwargs['product_variant']
            await db_session.merge(variant)

        OrderItemFactory._meta.sqlalchemy_session = db_session
        order_item = OrderItemFactory.build(**kwargs)
        db_session.add(order_item)
        await db_session.commit()
        await db_session.refresh(order_item)
        return order_item

    return _create_order_item


@pytest_asyncio.fixture
async def cart_item_factory(db_session, cart_factory, product_variant_factory):
    async def _create_cart_item(**kwargs):
        if 'cart' not in kwargs:
            kwargs['cart'] = await cart_factory()
        else:
            cart = kwargs['cart']
            await db_session.merge(cart)

        if 'variant' not in kwargs:
            kwargs['variant'] = await product_variant_factory()
        else:
            variant = kwargs['variant']
            await db_session.merge(variant)

        CartItemFactory._meta.sqlalchemy_session = db_session
        cart_item = CartItemFactory.build(**kwargs)
        db_session.add(cart_item)
        await db_session.commit()
        await db_session.refresh(cart_item)
        return cart_item

    return _create_cart_item


# Auth token fixture
@pytest_asyncio.fixture
async def auth_token(client, user_factory):
    user = await user_factory(email="test@example.com")
    response = await client.post(
        "/api/users/login",
        data={"username": user.email, "password": "password123"}
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}