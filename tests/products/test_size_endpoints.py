import pytest


@pytest.fixture()
def size_payload(faker):
    return {
        "label": faker.lexify(text="??"),
    }


@pytest.mark.asyncio
async def test_create_size(client, size_payload):
    response = await client.post("/api/sizes/", json=size_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["label"] == size_payload["label"]


@pytest.mark.asyncio
async def test_get_size(client, size_factory):
    size = await size_factory()
    response = await client.get(f"/api/sizes/{size.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == size.id
    assert data["label"] == size.label


@pytest.mark.asyncio
async def test_get_sizes(client, size_factory):
    await size_factory()
    await size_factory()
    await size_factory()

    response = await client.get("/api/sizes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_size(client, size_factory):
    size = await size_factory()
    updated_payload = {
        "label": "XL",
    }
    response = await client.put(f"/api/sizes/{size.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == size.id
    assert data["label"] == updated_payload["label"]


@pytest.mark.asyncio
async def test_partial_update_size(client, size_factory):
    size = await size_factory()
    partial_payload = {
        "label": "XXL",
    }
    response = await client.patch(f"/api/sizes/{size.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == size.id
    assert data["label"] == partial_payload["label"]


@pytest.mark.asyncio
async def test_delete_size(client, size_factory, auth_headers):
    size = await size_factory()
    response = await client.delete(f"/api/sizes/{size.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_size_unauthorized(client, size_factory):
    size = await size_factory()
    response = await client.delete(f"/api/sizes/{size.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_size(client):
    response = await client.get("/api/sizes/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Size not found"