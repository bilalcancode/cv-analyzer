import os

import pytesseract
from docx import Document
from pdf2image import convert_from_path


def extract_text_from_pdf(file_path):
    """
    Convert PDF pages to images and use Tesseract OCR to extract text.
    """
    try:
        images = convert_from_path(file_path)
    except Exception as e:
        raise Exception(f"Error converting PDF: {e}")

    text = ""
    for image in images:
        # You can adjust pytesseract configuration if needed.
        text += pytesseract.image_to_string(image)
    return text


def extract_text_from_docx(file_path):
    """
    Extract text from a .docx file using python-docx.
    """
    try:
        doc = Document(file_path)
    except Exception as e:
        raise Exception(f"Error processing DOCX: {e}")

    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text(file_path):
    """
    Determine the file type and extract text accordingly.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        # Note: python-docx primarily supports .docx. For .doc files, additional handling might be needed.
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file extension for OCR extraction")
