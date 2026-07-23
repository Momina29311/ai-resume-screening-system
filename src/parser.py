from pathlib import Path
import logging

import pdfplumber
from pypdf import PdfReader

from .utils import create_directory, write_text, log_message

logger = logging.getLogger(__name__)


def validate_pdf(pdf_path: str) -> bool:
    path = Path(pdf_path)
    return path.is_file() and path.suffix.lower() == ".pdf"

def extract_text_from_pdf(pdf_path: str) -> str:
    if not validate_pdf(pdf_path):
        raise FileNotFoundError(f"Invalid PDF path: {pdf_path}")

    reader = PdfReader(pdf_path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()

def extract_pages(pdf_path: str) -> list[str]:
    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages
    try:
        logger.info("Reading resume: %s", pdf_path)

        pages = extract_pages(pdf_path)
        logger.info("Number of pages: %s", len(pages))

        text = "\n".join(pages).strip()

        if not text:
            reader = PdfReader(pdf_path)
            fallback_text = []
            for page in reader.pages:
                fallback_text.append(page.extract_text() or "")
            text = "\n".join(fallback_text).strip()

        logger.info("Text extracted successfully")
        logger.info("Characters extracted: %s", len(text))
        return text

    except Exception:
        logger.exception("Failed to extract PDF text")
        raise


def save_extracted_text(pdf_path: str, output_dir: str = "data/processed") -> str:
    create_directory(output_dir)
    text = extract_text_from_pdf(pdf_path)
    output_path = Path(output_dir) / f"{Path(pdf_path).stem}.txt"
    write_text(str(output_path), text)
    log_message(f"Saved extracted text to {output_path}")
