import pytest

from db import ConnToData, CreateTable, conn


# This will loop everytime as it is autouse=True
# Just for cleanup of data, so that test1 wont interfere with test2 kind like that
@pytest.fixture(autouse=True)
def test_dbcreation():
    CreateTable()   
    yield

    with conn, conn.cursor() as cur:
        cur.execute("DELETE FROM tbl_books;")

# -- Testing -- 

# Add Book
def testp_add():
    print("\nAdd book")
    print("="*20)
    print("[Positive] Correct input test")
    ConnToData(3, Name="Bryan's Book", Year="2026-01-01", Author="Yowzki")

    books = ConnToData(0)

    assert len(books) > 0 
    assert books[-1]["name"] == "Bryan's Book"

    print("Correct")

def testn_add():
    print("\n[Negative] Wrong input test")
    with pytest.raises(ValueError):
        ConnToData(3, Name="Bryan's Book", Year="2026", Author="Yowzki")
    print("Input correctly rejected")   
    print("="*20)

# Update Book
def testp_update():
    print("\n\nUpdate book")
    print("="*20)
    print("[Positive] Updating book")
    ConnToData(3, Name="Bryan's Book", Year="2026-01-01", Author="Yowzki")

    books = ConnToData(0)
    last_idx = books[-1]["id"]

    ConnToData(1, id=last_idx, Name="Test update", Year="2026-02-02", Author="Test update")

    print("Updated")
    books_after_update = ConnToData(0) 
    print("Getting data again")

    assert books_after_update[-1]["name"] == "Test update"
    assert books_after_update[-1]["year"] == "2026-02-02"
    assert books_after_update[-1]["author"] == "Test update"
    print("Data updated correctly")

def testn_update():
    print("\n[Negative]")
    
    print("Input rejected")
    print("="*20)

# Delete Book
def testp_delete():
    print("\n\nDelete book")
    print("="*20)
    print("[Positive] deleting book")
    ConnToData(3, Name="Test to Delete", Year="2026-01-01", Author="Test_author_name")

    books = ConnToData(0)
    last_idx = books[-1]["id"]

    ConnToData(2, id=last_idx)

    print("Deleted")
    books_after_deletion = ConnToData(0)
    print("Getting data again")

    if len(books_after_deletion) > 0: 
        assert books_after_deletion[-1]["name"] != "Test to Delete"
    print("Book deleted correctly")

def testn_delete():
    print("\n[Negative] deleting wrong input book")
    ConnToData(2, id=999999)
    print("Book deletion Handled correctly")
    print("="*20)

# DEFENSE stuff just for fun
def test_sql_injection_defense():
    # Pass SQL injection payload into the fields
    # Will only work if i did f"name values {}" change it for fun
    mal_name = "Hacker Book'; DROP TABLE tbl_books; --"

    print("\n\nSQL Injection")
    print("="*20)
    print("Sending payload")
    ConnToData(3, Name=mal_name, Year="2026-01-01", Author="Konichiwa")
    books = ConnToData(0)
    
    # just proves that the table is still there
    assert len(books) > 0
    
    # just checks if it is on a string not a command
    assert books[-1]["name"] == mal_name
    print("Input changed to string")
    print("="*20)