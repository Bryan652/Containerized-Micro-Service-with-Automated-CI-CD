import os
import psycopg2
from flask import jsonify
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host=os.getenv("DB_HOST"),
                        dbname=os.getenv("POSTGRES_NAME"),
                        user=os.getenv("POSTGRES_USER"),
                        password=os.getenv("POSTGRES_PASSWORD"),
                        port=int(os.getenv("DB_PORT")))

def CreateTable():
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS tbl_books (
                    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    Name VARCHAR(255),
                    Year DATE,
                    Author VARCHAR (255)
                )""")

def GetDataFromTable():
    with conn.cursor() as cur:
        cur.execute("""SELECT row_to_json(t) FROM (SELECT * FROM tbl_books) t;""")
        data = [row[0] for row in cur.fetchall()]
    return data

def UpdateDataFromTable(id, Name, Year, Author):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE tbl_books 
                SET 
                    Name = %s,
                    Year = %s,
                    Author = %s
                WHERE id = %s;
            """, (Name, Year, Author, id))

def DeleteDataFromTable(id):
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tbl_books WHERE id = %s;", (id,))

def AddDataFromTable(Name, Year, Author):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tbl_books (Name, Year, Author)
                VALUES (%s, %s, %s)
            """, (Name, Year, Author))

# How to make this optional?? The id name year and author
def ConnToData(cond, id=None, Name=None, Year=None, Author=None):
    if cond == 0:
        return GetDataFromTable() 
    if cond == 1:
        UpdateDataFromTable(id, Name, Year, Author)
    if cond == 2:
        DeleteDataFromTable(id)
    if cond == 3:
        AddDataFromTable(Name, Year, Author)