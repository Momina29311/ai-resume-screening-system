from pathlib import Path
import tempfile

import streamlit as st

from src.parser import extract_text_from_pdf, save_extracted_text

st.set_page_config(page_title="Resume Screening System", layout="wide")
st.title("Resume Screening System")
st.write("Upload a PDF resume to extract text and save a .txt copy.")

uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])

col1, col2 = st.columns(2)
run_parse = col1.button("Parse Resume", type="primary")
clear_btn = col2.button("Clear")

if clear_btn:
    st.rerun()

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")

    if run_parse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            text = extract_text_from_pdf(tmp_path)
            save_path = save_extracted_text(tmp_path)

            st.success("Resume parsed successfully.")
            st.write(f"Characters extracted: {len(text)}")
            st.write(f"Words extracted: {len(text.split())}")

            st.subheader("Preview")
            st.text_area("Extracted text", text, height=400)

            st.info(f"Saved extracted text to: {save_path}")

            st.download_button(
                label="Download extracted text",
                data=text,
                file_name=Path(uploaded_file.name).stem + ".txt",
                mime="text/plain",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)
else:
    st.info("Upload a PDF to begin.")