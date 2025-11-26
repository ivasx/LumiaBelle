import pytest
from datetime import datetime


@pytest.fixture()
def user_payload(faker):
    return {
        "email": faker.email(),
        "password": "password123",
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "phone_number": f"+38050{faker.random_int(1000000, 9999999)}",
        "is_active": True,
    }


@pytest.mark.asyncio
async def test_create_user(client, user_payload):
    response = await client.post("/api/users/", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert data["first_name"] == user_payload["first_name"]
    assert data["last_name"] == user_payload["last_name"]
    assert data["phone_number"] == user_payload["phone_number"]
    assert data["is_active"] == user_payload["is_active"]
    assert "hashed_password" in data
    assert data["hashed_password"] != user_payload["password"]


@pytest.mark.asyncio
async def test_login_user(client, user_factory):
    user = await user_factory(email="login@test.com")
    response = await client.post(
        "/api/users/login",
        data={"username": user.email, "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, user_factory):
    user = await user_factory(email="test@test.com")
    response = await client.post(
        "/api/users/login",
        data={"username": user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_user(client, user_factory):
    user = await user_factory()
    response = await client.get(f"/api/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name


@pytest.mark.asyncio
async def test_get_users(client, user_factory):
    await user_factory()
    await user_factory()
    await user_factory()

    response = await client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_user(client, user_factory, faker):
    user = await user_factory()
    updated_payload = {
        "email": faker.email(),
        "password": "newpassword123",
        "first_name": "Updated",
        "last_name": "Name",
        "phone_number": "+380501234567",
        "is_active": False,
    }
    response = await client.put(f"/api/users/{user.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == updated_payload["email"]
    assert data["first_name"] == updated_payload["first_name"]
    assert data["last_name"] == updated_payload["last_name"]
    assert data["is_active"] == updated_payload["is_active"]


@pytest.mark.asyncio
async def test_partial_update_user(client, user_factory):
    user = await user_factory()
    partial_payload = {
        "first_name": "PartialUpdate",
    }
    response = await client.patch(f"/api/users/{user.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["first_name"] == partial_payload["first_name"]
    assert data["email"] == user.email


@pytest.mark.asyncio
async def test_delete_user(client, user_factory, auth_headers):
    user = await user_factory()
    response = await client.delete(f"/api/users/{user.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_unauthorized(client, user_factory):
    user = await user_factory()
    response = await client.delete(f"/api/users/{user.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_user(client):
    response = await client.get("/api/users/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"