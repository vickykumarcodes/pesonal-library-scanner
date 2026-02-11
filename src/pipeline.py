from src.barcode import extract_isbn
from src.book_api import fetch_book_metadata
from src.database import insert_book

def scan_only(image_path):
    isbn = extract_isbn(image_path)
    if not isbn:
        return None
    return fetch_book_metadata(isbn)

def normalize_authors(authors):
    if isinstance(authors, list):
        return ", ".join(authors)
    if isinstance(authors, str):
        return authors.strip()
    return "Unknown"

def scan_and_store(image_path):
    book = scan_only(image_path)
    if not book:
        return {"stored": False}

    # 🔥 NORMALIZE AUTHORS HERE (STEP 3)
    book["authors"] = normalize_authors(book.get("authors"))

    stored = insert_book(book)

    return {
        "stored": stored,
        "isbn": book["isbn"]
    }

