import psycopg2.errors
import pytest

from db import ConnToData, CreateTable, conn


# This will loop everytime as it is autouse=True
# Just for cleanup of data, so that test1 wont interfere with test2 kind like that
@pytest.fixture(autouse=True)
def clean_db():
    CreateTable()   
    with conn, conn.cursor() as cur:
        cur.execute("DELETE FROM tbl_books;")
    yield
    with conn, conn.cursor() as cur:
            cur.execute("DELETE FROM tbl_books;")

# -- Testing -- 

# Add Book
def test_add_correct_data():
    ConnToData(3, Name="Bryan's Book", Year="2026-01-01", Author="Yowzki")

    books = ConnToData(0)

    assert len(books) > 0 
    assert books[-1]["name"] == "Bryan's Book"

def test_add_invalid_year():
    with pytest.raises(psycopg2.errors.InvalidDatetimeFormat):
        ConnToData(3, Name="Bryan's Book", Year="2026", Author="Yowzki")

# Update Book
def test_update_book():
    ConnToData(3, Name="Bryan's Book", Year="2026-01-01", Author="Yowzki")

    books = ConnToData(0)
    last_idx = books[-1]["id"]

    ConnToData(1, id=last_idx, Name="Test update", Year="2026-02-02", Author="Test update")

    books_after_update = ConnToData(0) 

    assert books_after_update[-1]["name"] == "Test update"
    assert books_after_update[-1]["year"] == "2026-02-02"
    assert books_after_update[-1]["author"] == "Test update"

# Delete Book
def test_delete_book():
    ConnToData(3, Name="Test to Delete", Year="2026-01-01", Author="Test_author_name")

    books = ConnToData(0)
    last_idx = books[-1]["id"]

    ConnToData(2, id=last_idx)

    assert all(b["id"] != last_idx for b in ConnToData(0))

def test_delete_nonexistent_book():
    count_before = len(ConnToData(0))
    ConnToData(2, id=999999)
    assert len(ConnToData(0)) == count_before

# DEFENSE stuff just for fun
def test_sql_injection_defense():
    # Pass SQL injection payload into the fields
    # Will only work if i did f"name values {}" change it for fun
    mal_name = "Hacker Book'; DROP TABLE tbl_books; --"

    ConnToData(3, Name=mal_name, Year="2026-01-01", Author="Konichiwa")
    books = ConnToData(0)
    
    # just proves that the table is still there
    assert len(books) > 0
    
    # just checks if it is on a string not a command
    assert books[-1]["name"] == mal_name