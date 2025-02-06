import streamlit as st
import requests
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_SUMMARY_URL = "https://api.deepseek.com/summarize"
DEEPSEEK_GENERATE_URL = "https://api.deepseek.com/generate"

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function to summarize text using Deepseek
def summarize_text(text):
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {"text": text, "max_length": 200}
    response = requests.post(DEEPSEEK_SUMMARY_URL, json=payload, headers=headers)
    return response.json().get("summary", "Summarization failed.")

# Function to generate answers using Deepseek
def generate_answer(context, question):
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {"context": context, "question": question}
    response = requests.post(DEEPSEEK_GENERATE_URL, json=payload, headers=headers)
    return response.json().get("answer", "Answer generation failed.")

# Streamlit UI
st.title("RAG Agent with Deepseek")
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    document_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Text Preview")
    st.text_area("Document Content", document_text[:1000] + "...", height=200)
    
    if st.button("Summarize Document"):
        summary = summarize_text(document_text)
        st.subheader("Document Summary")
        st.write(summary)
    
    question = st.text_input("Ask a question about the document")
    if question:
        answer = generate_answer(document_text, question)
        st.subheader("Answer")
        st.write(answer)
