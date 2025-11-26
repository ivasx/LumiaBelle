import pytest
import pytest_asyncio


@pytest_asyncio.fixture()
async def address_payload(faker, user_factory):
    user = await user_factory()
    return {
        "user_id": user.id,
        "address_line1": faker.street_address(),
        "city": faker.city(),
        "zip_code": faker.zipcode(),
        "is_default": False,
    }


@pytest.mark.asyncio
async def test_create_user_address(client, address_payload):
    response = await client.post("/api/user_addresses/", json=address_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == address_payload["user_id"]
    assert data["address_line1"] == address_payload["address_line1"]
    assert data["city"] == address_payload["city"]
    assert data["zip_code"] == address_payload["zip_code"]
    assert data["is_default"] == address_payload["is_default"]


@pytest.mark.asyncio
async def test_get_user_address(client, user_address_factory):
    address = await user_address_factory()
    response = await client.get(f"/api/user_addresses/{address.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == address.id
    assert data["user_id"] == address.user_id
    assert data["address_line1"] == address.address_line1
    assert data["city"] == address.city
    assert data["zip_code"] == address.zip_code


@pytest.mark.asyncio
async def test_get_user_addresses(client, user_address_factory):
    await user_address_factory()
    await user_address_factory()
    await user_address_factory()

    response = await client.get("/api/user_addresses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_user_address(client, user_address_factory, faker):
    address = await user_address_factory()
    updated_payload = {
        "user_id": address.user_id,
        "address_line1": "Updated Street 123",
        "city": "Updated City",
        "zip_code": "12345",
        "is_default": True,
    }
    response = await client.put(f"/api/user_addresses/{address.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == address.id
    assert data["address_line1"] == updated_payload["address_line1"]
    assert data["city"] == updated_payload["city"]
    assert data["zip_code"] == updated_payload["zip_code"]
    assert data["is_default"] == updated_payload["is_default"]


@pytest.mark.asyncio
async def test_partial_update_user_address(client, user_address_factory):
    address = await user_address_factory()
    partial_payload = {
        "city": "Partially Updated City",
    }
    response = await client.patch(f"/api/user_addresses/{address.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == address.id
    assert data["city"] == partial_payload["city"]
    assert data["address_line1"] == address.address_line1


@pytest.mark.asyncio
async def test_delete_user_address(client, user_address_factory, auth_headers):
    address = await user_address_factory()
    response = await client.delete(f"/api/user_addresses/{address.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_address_unauthorized(client, user_address_factory):
    address = await user_address_factory()
    response = await client.delete(f"/api/user_addresses/{address.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_user_address(client):
    response = await client.get("/api/user_addresses/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Address not found"