import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "library.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT,
            authors TEXT,
            publisher TEXT,
            published_date TEXT,
            source TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()

def insert_book(book):
    """
    Inserts a book into the database.
    Returns True if inserted, False if already exists.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO books (isbn, title, authors, publisher, published_date, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                book["isbn"],
                book["title"],
                ", ".join(book["authors"]),
                book.get("publisher"),
                book.get("published_year"),
                book.get("source", "unknown"),
            ),
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # ISBN already exists
        return False

    finally:
        conn.close()


def save_book(book):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO books
        (isbn, title, authors, publisher, published_date, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
            book["isbn"],
            book.get("title"),
            ", ".join(book.get("authors", [])),
            book.get("publisher"),
            book.get("publishedDate") or book.get("published_date"),
            book.get("source", "unknown")
    ))

    conn.commit()
    conn.close()

def search_books(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM books
    WHERE title LIKE ?
        OR authors LIKE ?
        OR isbn LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    rows = cur.fetchall()
    conn.close()
    return rows

def delete_book(isbn):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE isbn = ?",
        (isbn,)
    )

    conn.commit()
    conn.close()

