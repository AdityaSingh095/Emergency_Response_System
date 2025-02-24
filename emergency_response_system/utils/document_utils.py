import PyPDF2
import streamlit as st

def process_pdf(pdf_file):
    if not pdf_file:
        return ""

    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return ""
