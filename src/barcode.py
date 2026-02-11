import cv2
from pyzbar.pyzbar import decode


def extract_isbn(image_path):
    """
    Extract ISBN barcode from an image.
    Returns ISBN string or None.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None

    barcodes = decode(image)
    for barcode in barcodes:
        data = barcode.data.decode("utf-8")
        if data.isdigit() and (len(data) == 10 or len(data) == 13):
            return data

    return None

