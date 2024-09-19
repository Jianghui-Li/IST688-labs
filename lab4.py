import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb

client = chromadb.PersistentClient(path="pdfs")

collection = client.get_or_create_collection(name="Lab4Collection")

if 'openai_client' not in st.session_state:
    api_key = st.secrets["API_KEY"]
    st.session_state.openai_client = OpenAI(api_key=api_key)

if 'Lab4_vectorDB' not in st.session_state:
    st.session_state.Lab4_vectorDB = collection

def add_to_collection(collection, text, filename):
    openai_client = st.session_state.openai_client
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding

    collection.add(
        documents=[text],
        ids=[filename],
        embeddings=[embedding]
    )

def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
    return text

pdf_directory = "pdfs/"
pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

if not st.session_state.get('pdfs_added', False):
    for pdf_file in pdf_files:
        text_content = read_pdf(pdf_file)
        filename = os.path.basename(pdf_file)
        add_to_collection(st.session_state.Lab4_vectorDB, text_content, filename)
    st.session_state.pdfs_added = True

topic = st.sidebar.selectbox("Topic", ("Text Mining", "GenAI"))

openai_client = st.session_state.openai_client
response = openai_client.embeddings.create(
    input=topic,
    model="text-embedding-3-small"
)

query_embedding = response.data[0].embedding

results = st.session_state.Lab4_vectorDB.query(
    query_embeddings=[query_embedding],
    n_results=3
)

for i in range(len(results['documents'][0])):
    doc_id = results['ids'][0][i]
    st.write(f"The following file/syllabus might be helpful: {doc_id}")
