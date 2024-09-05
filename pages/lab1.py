import streamlit as st
from openai import OpenAI
import PyPDF2

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.title("Upload Document and Ask Questions")

# Ask for the OpenAI API key from the main app's input.
openai_api_key = st.session_state.get('openai_api_key')
if not openai_api_key:
    st.warning("Please enter your OpenAI API key on the main page.")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=("txt", "pdf"))

    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'txt':
            document = uploaded_file.read().decode()
        elif file_extension == 'pdf':
            document = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file type.")
            document = None
    else:
        document = None

    question = st.text_area("Ask a question about the document!", disabled=not document)

    if document and question:
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]
        
        # Generate an answer using OpenAI API (Assuming GPT model)
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # Stream the response
        st.write_stream(stream)
