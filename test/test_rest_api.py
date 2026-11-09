import pytest

from API import BookAPI
from db import CreateTable


@pytest.fixture
def client():
    CreateTable()
    BookAPI.config["TESTING"] = True
    with BookAPI.test_client() as client:
        yield client

def test_api_main_route(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def get_data(client):
    payload = {
        "Name":"Test Added Book",
        "Year":"2026-01-01",
        "Author": "Test Added Author"
    }

    response = client.post("/api/books", json=payload)
    data = response.get_json()

    return data

def test_api_add_route(client):
    payload = {
        "Name":"Test Added Book",
        "Year":"2026-01-01",
        "Author": "Test Added Author"
    }

    response = client.post("/api/books", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert "Message" in data
    assert "data" in data
    assert data["Message"] == "Book added successfully" # This is case sensitive

def test_api_add_missing_required_field_route(client):
    payload = {
        "Name":"Test Added Book",
        "Year":"2026-01-01",
    }

    response = client.post("/api/books", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields" # This is case sensitive

def test_api_add_invalid_data_format_route(client):
    payload = {
        "Name":"Test Added Book",
        "Year":"2026",
        "Author": "Test Added Author"
    }

    response = client.post("/api/books", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid date/year format (YYYY-DD-MM)" # This is case sensitive

def test_api_update_correct_route(client):
    data = get_data(client)

    id = data["data"]["id"]

    payload_update = {
        "Name":"Test Update Name",
        "Year":"2026-01-01",
        "Author":"Test Update Author"
    }

    response_update = client.put(f"/api/books/{id}", json=payload_update)

    assert response_update.status_code == 200
    updated_data = response_update.get_json()
    assert "Message" in updated_data
    assert "data" in updated_data
    assert updated_data["Message"] == "Book updated successfully"

def test_api_update_wrong_id_route(client):
    id = 99999

    payload_update = {
        "Name":"Test Update Name",
        "Year":"2026-01-01",
        "Author":"Test Update Author"
    }

    response_update = client.put(f"/api/books/{id}", json=payload_update)

    assert response_update.status_code == 404
    updated_data = response_update.get_json()
    assert "error" in updated_data
    assert updated_data["error"] == f"No specific book with id {id} found"

def test_api_update_invalid_date_format_route(client):
    data = get_data(client)

    id = data["data"]["id"]

    payload_update = {
        "Name":"Test Update Name",
        "Year":"2026",
        "Author":"Test Update Author"
    }

    response_update = client.put(f"/api/books/{id}", json=payload_update)

    assert response_update.status_code == 400
    updated_data = response_update.get_json()
    assert "error" in updated_data
    assert updated_data["error"] == "Invalid date/year format (YYYY-DD-MM)"

def test_api_delete_correct_id_route(client):
    data = get_data(client)

    id = data["data"]["id"]

    delete_response = client.delete(f"/api/books/{id}")

    assert delete_response.status_code == 200
    data = delete_response.get_json()
    assert "Message" in data
    assert data["Message"] == f"Book {id} successfully deleted"

def test_api_delete_wrong_id_route(client):
    id = 99999
    delete_response = client.delete(f"/api/books/{id}")

    assert delete_response.status_code == 404
    data = delete_response.get_json()
    assert "error" in data
    assert data["error"] == f"No specific book with id {id} found"
#endregion