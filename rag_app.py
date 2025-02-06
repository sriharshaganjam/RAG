import streamlit as st
import os
import requests
from PyPDF2 import PdfReader
from io import StringIO

# Deepseek API credentials (replace with your actual API key)
DEEPSEEK_API_KEY = "your_deepseek_api_key"
DEEPSEEK_SUMMARIZATION_URL = "https://api.deepseek.com/v1/summarize"
DEEPSEEK_TEXT_GENERATION_URL = "https://api.deepseek.com/v1/generate"

# Streamlit app title
st.title("📄 RAG Agent with Deepseek APIs")
st.write("Upload documents, ask questions, and get answers powered by Deepseek!")

# File uploader for documents
uploaded_files = st.file_uploader("Upload your documents (PDF or text)", type=["pdf", "txt"], accept_multiple_files=True)

# Function to extract text from uploaded files
def extract_text_from_files(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text += stringio.read()
    return text

# Function to call Deepseek Summarization API
def summarize_text(text):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "max_length": 150  # Adjust summary length as needed
    }
    response = requests.post(DEEPSEEK_SUMMARIZATION_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("summary", "Summary not available.")
    else:
        st.error(f"Error in summarization: {response.status_code}")
        return None

# Function to call Deepseek Text Generation API
def generate_answer(question, context):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:",
        "max_tokens": 200  # Adjust response length as needed
    }
    response = requests.post(DEEPSEEK_TEXT_GENERATION_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("text", "Answer not available.")
    else:
        st.error(f"Error in text generation: {response.status_code}")
        return None

# Process uploaded files
if uploaded_files:
    # Extract text from uploaded files
    text = extract_text_from_files(uploaded_files)
    st.subheader("Extracted Text")
    st.write(text[:1000] + "...")  # Display first 1000 characters for preview

    # Summarize the text using Deepseek API
    st.subheader("Document Summary")
    summary = summarize_text(text)
    if summary:
        st.write(summary)

    # Question answering section
    st.subheader("Ask a Question")
    question = st.text_input("Enter your question about the document:")
    if question:
        # Generate answer using Deepseek API
        answer = generate_answer(question, text)
        if answer:
            st.subheader("Answer")
            st.write(answer)
else:
    st.write("Please upload documents to get started.")
