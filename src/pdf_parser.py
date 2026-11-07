"""
PDF text extraction module.

This module provides functionality to extract text content from PDF files
using PyMuPDF (fitz) library.
"""

import pymupdf  # PyMuPDF
from typing import Optional
from pathlib import Path


def extract_text_from_pdf(pdf_path: str,doc_secrets: dict[str,str]) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file to process

    Returns:
        str: Extracted text content from all pages

    Raises:
        Exception: If PDF cannot be opened or processed
    """
    try:
        doc = pymupdf.open(pdf_path)
        path = Path(pdf_path)

        # Handle password-protected files
        if doc.needs_pass:
            password=doc_secrets.get(path.name)
            if not password:
                print(f"Error reading {pdf_path}: file is password protected but no password was provided")
                return ""
            if not doc.authenticate(password):  # returns 0 on wrong password
                print(f"Error reading {pdf_path}: incorrect password")
                return ""
        text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
            text += "\n"  # Add page separator

        doc.close()
        return text.strip()

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def validate_pdf_file(pdf_path: str) -> bool:
    """
    Validate that the file is a readable PDF.

    Args:
        pdf_path: Path to the PDF file to validate

    Returns:
        bool: True if file is a valid PDF, False otherwise
    """
    try:
        doc = pymupdf.open(pdf_path)
        page_count = len(doc)
        doc.close()
        return page_count > 0
    except Exception:
        return False