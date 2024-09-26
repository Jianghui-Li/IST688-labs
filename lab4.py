import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb

client = chromadb.PersistentClient(path="pdfs")

def get_pdf_files():
    pdf_directory = "pdfs/"
    return [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

if 'Lab4_vectorDB' not in st.session_state:
    try:
        collection = client.get_collection(name="Lab4Collection")
    except chromadb.errors.CollectionNotFoundError:
        collection = client.create_collection(name="Lab4Collection", metadata={"hnsw:space": "cosine"})
    st.session_state.Lab4_vectorDB = collection
else:
    collection = st.session_state.Lab4_vectorDB

if 'openai_client' not in st.session_state:
    api_key = st.secrets["API_KEY"]
    st.session_state.openai_client = OpenAI(api_key=api_key)

def add_to_collection(collection, text, filename):
    openai_client = st.session_state.openai_client
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding

    existing_ids = collection.get()["ids"]
    if filename in existing_ids:
        collection.update(
            ids=[filename],
            documents=[text],
            metadatas=[{"source": filename}],
            embeddings=[embedding]
        )
        st.write(f"Updated in collection: {filename}")
    else:
        collection.add(
            documents=[text],
            metadatas=[{"source": filename}],
            ids=[filename],
            embeddings=[embedding]
        )
        st.write(f"Added to collection: {filename}")

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

pdf_files = [os.path.join("pdfs/", f) for f in get_pdf_files()]
existing_ids = collection.get()["ids"]
if len(existing_ids) < len(pdf_files):
    st.write("Processing PDF files:")
    progress_bar = st.progress(0)
    total_files = len(pdf_files)
    for idx, pdf_file in enumerate(pdf_files):
        text_content = read_pdf(pdf_file)
        filename = os.path.basename(pdf_file)
        st.write(f"Processing file: {filename}")
        add_to_collection(st.session_state.Lab4_vectorDB, text_content, filename)
        progress_bar.progress((idx + 1) / total_files)
else:
    st.write("PDFs already added to the collection. Skipping reprocessing.")

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that retrieves relevant documents based on user input."},
        {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ]

def limit_conversation_memory(messages):
    return messages[-5:]

def handle_user_input(prompt):
    openai_client = st.session_state.openai_client

    response = openai_client.embeddings.create(
        input=prompt,
        model="text-embedding-3-small"
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    augmented_info = "I found the following relevant documents:\n"
    for i in range(len(results['documents'][0])):
        doc_id = results['ids'][0][i]
        augmented_info += f"- {doc_id}\n"

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": augmented_info})
    
    return augmented_info

st.title("Document Retrieval Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    response = handle_user_input(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
