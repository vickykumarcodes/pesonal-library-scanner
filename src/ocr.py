import cv2
import sys
import re
import pytesseract
import os
from pyzbar.pyzbar import decode, ZBarSymbol

# silence zbar warnings.
sys.stderr = open(os.devnull, 'w')

def scan_barcode(image_path):
    img = cv2.imread(str(image_path))

    if img is None:
        raise ValueError("Image not loaded. Check path.")

    # --- Strategy 1: Raw image ---
    decoded = decode(img, symbols=[ZBarSymbol.EAN13])
    if decoded:
        return _extract_isbn(decoded)

    # --- Strategy 2: Grayscale ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    decoded = decode(gray)
    if decoded:
        return _extract_isbn(decoded)

    # --- Strategy 3: High contrast (thresholding) ---
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    decoded = decode(thresh)
    if decoded:
        return _extract_isbn(decoded)

    # OCR fallback
    return scan_isbn_text(image_path)



def _extract_isbn(decoded_objects):
    for obj in decoded_objects:
        code = obj.data.decode("utf-8")
        if code.startswith(("978", "979")):
            return code
    return None

def scan_isbn_text(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return None

    # Preprocess for OCR
    cropped = crop_isbn_region(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray)

    # try ISBN-13 first
    isbn13 = extract_isbn_from_text(text)
    if isbn13:
        return isbn13

    # try ISBN-10
    isbn10 = extract_isbn10_from_text(text)
    if isbn10:
        return isbn10_to_isbn13(isbn10)

    return None


def extract_isbn_from_text(text):
    """
    ISBN 978-93-54352-80-5
    ISBN:9789354352805
    978 93 54352 80 5
    """

    candidates = re.findall(
        r"(97[89][-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d)",
        text
    )

    for raw in candidates:
        isbn = normalize_isbn(raw)
        if isbn and is_valid_isbn13(isbn):
            return isbn

    return None

def normalize_isbn(raw):
    isbn = re.sub(r"[^0-9]", "", raw)
    return isbn if len(isbn) == 13 else None

def is_valid_isbn13(isbn):
    total = 0
    for i, digit in enumerate(isbn[:12]):
        total += int(digit) * (1 if i % 2 == 0 else 3)

    check = (10 - (total % 10)) % 10
    return check == int(isbn[-1])

def extract_isbn10_from_text(text):
    """
    Matches ISBN-10
    ISBN 93-80703-31-7
    0-393-04002-X
    """

    candidates = re.findall(
            r"(?:ISBN[:\s]*)?(\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dX])",
            text,
            re.IGNORECASE

    )

    for raw in candidates:
        isbn10 = re.sub(r"[^0-9X]", "", raw)
        if len(isbn10) == 10 and is_valid_isbn10(isbn10):
            return isbn10

    return None

def is_valid_isbn10(isbn):
    total = 0
    for i, ch in enumerate(isbn):
        value = 10 if ch == "X" else int(ch)
        total += value * (10 - i)

    return total % 11 == 0

def isbn10_to_isbn13(isbn10):
    core = "978" + isbn10[:-1]

    total = 0
    for i, digit in enumerate(core):
        total += int(digit) * (1 if i % 2 == 0 else 3)

    check = (10 - (total % 10)) % 10
    return core + str(check)

def crop_isbn_region(img):
    h, w = img.shape[:2]

    # Step 1: Focus on bottom 35% of image
    bottom = img[int(h * 0.65):h, 0:w]

    gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 2: Edge detection(barcode friendly)
    edges = cv2.Canny(blur, 50, 150)

    # Step 3: Find countours
    contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Step 4: Find wide horizontal rectangles(barcode candidates)
    candidates = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        aspect_ratio = cw / float(ch)

        if aspect_ratio > 5 and cw > w * 0.4:
            candidates.append((x, y, cw, ch))

    if not candidates:
        return bottom

    # Step 5: Pick the largest candidate
    x, y, cw, ch = max(candidates, key=lambda b: b[2] *  b[3])

    # Expand crop slightly to include ISBN text
    pad = 20
    y0 = max(y - pad, 0)
    y1 = min(y + ch + pad, bottom.shape[0])

    return bottom[y0:y1, :]














    
