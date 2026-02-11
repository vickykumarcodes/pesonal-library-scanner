import streamlit as st
from PIL import Image
import tempfile

from src.database import init_db, insert_book, search_books, delete_book
from src.pipeline import scan_only

# -------------------------------
# Helper functions (ADD HERE)
# -------------------------------
def format_authors(authors):
    if isinstance(authors, list):
        return ", ".join(authors)
    if isinstance(authors, str):
        return authors
    return "Unknown"

# ---------------------------
# App Config
# ---------------------------
st.set_page_config(
    page_title="Personal Library Scanner",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Personal Library Scanner")
st.caption("Upload a photo of a book barcode, review details, and save it to your library.")

# ---------------------------
# Initialize Database (SAFE)
# ---------------------------
init_db()


# ---------------------------
# Upload Section
# ---------------------------
st.markdown("### 📤 Upload Book Barcode Image")

uploaded_file = st.file_uploader(
    "Upload book barcode image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=400)

    # Save temp image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        book = scan_only(tmp.name)

    if not book:
        st.error("❌ Could not detect ISBN or fetch book metadata.")
    else:
        st.markdown("### 📖 Book Found")

        # Compact book display
        st.markdown(
f"""
<h3 style="margin-bottom: 0.2em;">📘 {book.get('title', 'Unknown Title')}</h3>

<small>
👤 <b>Author:</b> {format_authors(book.get('authors'))}<br>
🏢 <b>Publisher:</b> {book.get('publisher', 'Unknown')}<br>
📅 <b>Year:</b> {book.get('published_year', 'Unknown')}<br>
🔢 <b>ISBN:</b> {book.get('isbn', 'Unknown')}
</small>
""",
unsafe_allow_html=True
)




        # Confirmation buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Save to Library"):
                saved = insert_book(book)
                if saved:
                    st.success("📚 Book saved successfully!")
                else:
                    st.warning("⚠️ Book already exists in your library.")

        with col2:
            if st.button("❌ Cancel"):
                st.info("Book was not saved.")


# ---------------------------
# Library Section
# ---------------------------
st.divider()
st.markdown("### 📚 My Library")

search_query = st.text_input(
    "Search by title / author / ISBN",
    placeholder="Start typing..."
)

books = search_books(search_query)

for book in books:
    book_id, isbn, title, authors, publisher, year, source, added_at = book

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown(
            f"""
            **{title}**  
            <small>
            👤 {authors} | 🏢 {publisher or 'Unknown'} | 📅 {year} | 🔢 {isbn}
            </small>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("🗑️ Delete", key=f"delete_{isbn}"):
            delete_book(isbn)
            st.success(f"Deleted: {title}")
            st.rerun()
        



