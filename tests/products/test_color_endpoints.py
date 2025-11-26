import pytest


@pytest.fixture()
def color_payload(faker):
    return {
        "name": faker.color_name(),
        "hex_code": faker.hex_color(),
    }


@pytest.mark.asyncio
async def test_create_color(client, color_payload):
    response = await client.post("/api/colors/", json=color_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == color_payload["name"]
    assert data["hex_code"] == color_payload["hex_code"]


@pytest.mark.asyncio
async def test_get_color(client, color_factory):
    color = await color_factory()
    response = await client.get(f"/api/colors/{color.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == color.id
    assert data["name"] == color.name
    assert data["hex_code"] == color.hex_code


@pytest.mark.asyncio
async def test_get_colors(client, color_factory):
    await color_factory()
    await color_factory()
    await color_factory()

    response = await client.get("/api/colors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_color(client, color_factory):
    color = await color_factory()
    updated_payload = {
        "name": "Updated Color",
        "hex_code": "#FF0000",
    }
    response = await client.put(f"/api/colors/{color.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == color.id
    assert data["name"] == updated_payload["name"]
    assert data["hex_code"] == updated_payload["hex_code"]


@pytest.mark.asyncio
async def test_partial_update_color(client, color_factory):
    color = await color_factory()
    partial_payload = {
        "name": "Partially Updated Color",
    }
    response = await client.patch(f"/api/colors/{color.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == color.id
    assert data["name"] == partial_payload["name"]
    assert data["hex_code"] == color.hex_code


@pytest.mark.asyncio
async def test_delete_color(client, color_factory, auth_headers):
    color = await color_factory()
    response = await client.delete(f"/api/colors/{color.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_color_unauthorized(client, color_factory):
    color = await color_factory()
    response = await client.delete(f"/api/colors/{color.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_color(client):
    response = await client.get("/api/colors/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Color not found"