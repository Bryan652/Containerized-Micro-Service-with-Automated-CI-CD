import pytest
from API import BookAPI
from db import ConnToData

@pytest.fixture
def client():
    BookAPI.config["TESTING"] = True
    with BookAPI.test_client() as client:
        yield client

def test_get_route(client):
    print("\n\nHome")
    print("="*20)
    print("Loading Home..")
    response = client.get("/")
    assert response.status_code == 200
    print("Home successfully loaded")
    print("="*20)

def test_add_book_route(client):
    print("\n\nAdding book")
    print("="*20)
    print("Adding books")
    
    response = client.post("/Add", data={
        "Name": "Test add",
        "Year": "2026-01-01",
        "Author": "Bryan"
    }, follow_redirects=True)

    assert response.status_code == 200
    print("Data added successfully via POST")
    print("="*20)

def test_update_route(client):
    print("\n\nUpdating a book")
    print("="*20)

    response = client.post("/Add", data={
        "Name": "Test add",
        "Year": "2026-01-01",
        "Author": "Bryan"
    }, follow_redirects=True)

    books = ConnToData(0)
    book_id = books[-1]["id"]

    response = client.post(f"/Update/{ book_id }", data={
        "Name":"Updated Name",
        "Year":"2026-03-03",
        "Author":"Updated Bryan"
    }, follow_redirects=True)

    assert response.status_code == 200
    print("Updated successfully via POST")
    print("="*20)

def test_delete_route(client):
    print("\n\nUpdating a book")
    print("="*20)

    response = client.post("/Add", data={
            "Name": "Test add",
            "Year": "2026-01-01",
            "Author": "Bryan"
    }, follow_redirects=True)

    books = ConnToData(0)
    book_id = books[-1]["id"]

    response = client.post(f"/Delete/{book_id}", follow_redirects=True)

    assert response.status_code == 200
    print("Deleted successfully via POST")
    print("="*20)