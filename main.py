from src.database import init_db, search_books
from src.pipeline import scan_and_store

try:
    init_db()

    result = scan_and_store("data/images/test_1.jpg")
    print("Scan result:", result)

    print("\nMy Library:")
    for book in search_books(""):
        print(book)

except Exception as e:
    import traceback
    traceback.print_exc()
