import requests

def normalize_year(published_date):
    if not published_date:
        return "Unknown"
    return str(published_date)[:4]

def fetch_book_by_isbn(isbn):
    # Try Google Books first
    book = fetch_book_google(isbn)
    if book:
        print("Found via Google Books")
        return book

    # Fallback to Open Library
    book = fetch_book_openlibrary(isbn)
    if book:
        print("Found via Open Library")
        return book

    print(f"No metadata found for ISBN {isbn}")
    return None

def fetch_book_google(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()
    if "items" not in data:
        return None

    book = data["items"][0]["volumeInfo"]

    return {
    "title": book.get("title"),
    "authors": book.get("authors", []),
    "publisher": book.get("publisher"),
    "published_year": normalize_year(book.get("publishedDate")),
    "isbn": isbn,
    "source": "google"
}

def fetch_book_openlibrary(isbn):
    url = (
        "https://openlibrary.org/api/books"
        f"?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()
    key = f"ISBN:{isbn}"

    if key not in data:
        return None

    book = data[key]

    return {
    "title": book.get("title"),
    "authors": [a["name"] for a in book.get("authors", [])],
    "publisher": (
        book["publishers"][0]["name"]
        if book.get("publishers") and len(book["publishers"]) > 0
        else None
    ),
    "published_year": normalize_year(book.get("publish_date")),
    "isbn": isbn,
    "source": "openlibrary"
}

def fetch_book_metadata(isbn):
    # Try Google Books first
    book = fetch_book_google(isbn)
    if book:
        return book

    # Fallback to Open Library
    book = fetch_book_openlibrary(isbn)
    if book:
        return book

    return None

