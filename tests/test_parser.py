import pytest
from src.parser import validate_pdf, extract_text_from_pdf


def test_validate_pdf_true():
    assert validate_pdf("data/resumes/simple_ats_resume.pdf") is True


def test_validate_pdf_false():
    assert validate_pdf("data/resumes/not_a_pdf.txt") is False


def test_extract_text_missing_file():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("data/resumes/missing.pdf")


def test_extract_text_empty_pdf():
    text = extract_text_from_pdf("data/resumes/empty.pdf")
    assert text == ""