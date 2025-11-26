import pytest


@pytest.fixture()
def category_payload(faker):
    return {
        "name": faker.word(),
    }


@pytest.mark.asyncio
async def test_create_category(client, category_payload):
    response = await client.post("/api/categories/", json=category_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_payload["name"]


@pytest.mark.asyncio
async def test_get_category(client, category_factory):
    category = await category_factory()
    response = await client.get(f"/api/categories/{category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category.id
    assert data["name"] == category.name


@pytest.mark.asyncio
async def test_get_categories(client, category_factory):
    await category_factory()
    await category_factory()
    await category_factory()

    response = await client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_category(client, category_factory):
    category = await category_factory()
    updated_payload = {
        "name": "Updated Category",
    }
    response = await client.put(f"/api/categories/{category.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category.id
    assert data["name"] == updated_payload["name"]


@pytest.mark.asyncio
async def test_partial_update_category(client, category_factory):
    category = await category_factory()
    partial_payload = {
        "name": "Partial Update Category",
    }
    response = await client.patch(f"/api/categories/{category.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category.id
    assert data["name"] == partial_payload["name"]


@pytest.mark.asyncio
async def test_delete_category(client, category_factory, auth_headers):
    category = await category_factory()
    response = await client.delete(f"/api/categories/{category.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_category_unauthorized(client, category_factory):
    category = await category_factory()
    response = await client.delete(f"/api/categories/{category.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_category(client):
    response = await client.get("/api/categories/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Category not found"