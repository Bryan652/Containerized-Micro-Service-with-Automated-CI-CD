from db import CreateTable, conn

INITIAL_BOOKS = [
    ("Children of Time", "2012-05-22", "Adrian Tchaikovsky"),
    ("Kafka on the Shore", "1967-09-12", "Haruki Murakami"),
    ("The Lord of the Rings", "1997-07-29", "J.R.R. Tolkien"),
    ("The Intelligent Investor", "1995-03-01", "Benjamin Graham"),
    ("The Art of War", "1000-01-01", "Sun Tzu")
]

def seed_database():
    CreateTable()

    with conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT (*) FROM tbl_books;")
        count = cur.fetchone()[0]

        if count > 0:
            print(f"Database already contains {count} data. Skipping seeding.")
            return

        print("Seeding initial data")
        cur.executemany("""
                INSERT INTO tbl_books (Name, Year, Author) 
                VALUES (%s, %s, %s)
            """, INITIAL_BOOKS)

        print(f"successfully seeded {len(INITIAL_BOOKS)} data into postgresql")