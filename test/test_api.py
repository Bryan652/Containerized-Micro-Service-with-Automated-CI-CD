import pytest

from API import BookAPI
from db import ConnToData, CreateTable


@pytest.fixture
def client():
    CreateTable()
    BookAPI.config["TESTING"] = True
    with BookAPI.test_client() as client:
        yield client

# NO UI


# WITH UI
def test_get_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_book_route(client):
    response = client.post("/add", data={
        "Name": "Test Name Add",
        "Year": "2026-01-01",
        "Author": "Test Auth Add"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Name Add" in response.data
    assert b"Test Auth Add" in response.data

def test_update_route(client):
    response = client.post("/add", data={
        "Name": "Test add",
        "Year": "2026-01-01",
        "Author": "Bryan"
    }, follow_redirects=True)

    books = ConnToData(0)
    book_id = books[-1]["id"]

    response = client.post(f"/update/{ book_id }", data={
        "Name":"Test Updated Name",
        "Year":"2026-03-03",
        "Author":"Test Updated Bryan"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Updated Name" in response.data
    assert b"Test Updated Bryan" in response.data

def test_delete_route(client):
    response = client.post("/add", data={
            "Name": "Test Remove Data",
            "Year": "2026-01-01",
            "Author": "Test Remove Auth Bryan"
    }, follow_redirects=True)

    books = ConnToData(0)
    book_id = books[-1]["id"]

    response = client.post(f"/delete/{book_id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Remove Data" not in response.data
    assert b"Test Remove Auth Bryan" not in response.data