## Demo
![App demo](screenshot/demo.png)

# 📚 Personal Library Scanner

A project I built to scan physical books using a barcode image, fetch their metadata from public APIs, and store them in a local searchable library.

The goal was to design a clean pipeline from image → ISBN → metadata → database, instead of just building a UI.

---

## 🔍 What it does

* Detects ISBN from a barcode image using `pyzbar`
* Falls back to OCR (Tesseract) if barcode detection fails
* Validates ISBN-13 using checksum logic
* Fetches metadata from:

  * Google Books API
  * Open Library API (fallback)
* Stores books in a local SQLite database
* Prevents duplicates using a UNIQUE ISBN constraint
* Provides a Streamlit interface to:

  * Upload barcode images
  * Review book details before saving
  * Search by title, author, or ISBN
  * Delete entries

---

## 🧠 Design Approach

The project is structured in layers:

UI (Streamlit)
↓
Pipeline (application logic)
↓
Services (OCR + API calls)
↓
Database (SQLite)

Each module has a single responsibility:

* `streamlit_app.py` → user interface
* `pipeline.py` → coordinates scanning and storing
* `barcode.py` / `ocr.py` → ISBN extraction
* `app.py` → external API communication
* `database.py` → database schema and CRUD operations

The idea was to keep components independent and easy to modify.

---

## 🧪 ISBN Validation

OCR output can be noisy.
To avoid storing invalid data:

1. A regex pattern loosely detects ISBN-like strings.
2. The text is normalized to digits only.
3. ISBN-13 checksum logic verifies correctness.

This prevents false positives from random 13-digit numbers.

---

## 🛠 Tech Stack

* Python
* OpenCV
* pyzbar
* pytesseract
* SQLite
* Streamlit
* Requests

---

## 🚀 How to Run

1. Install dependencies:
    pip install -r requirements.txt

2. Run the app:
    streamlit run streamlit_app.py

3. Upload a book barcode image and test.

---
📌 Why I Built This

I built this mainly for myself.

I have a personal physical library and wanted a simple way to digitize it without manually typing every book entry. Scanning barcodes felt more natural and scalable than entering titles one by one.

At the same time, I used this as an opportunity to practice:

-> Working with computer vision libraries
-> Handling messy OCR output
-> Validating data using checksum algorithms
-> Designing a layered backend structure
-> Integrating external APIs with a local database

So this project solves a my personal need while also serving as a project for my portfolio.