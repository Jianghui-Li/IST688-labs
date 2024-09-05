import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("My Document Question Answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Access the API key from st.secrets
openai_api_key = st.secrets["API_KEY"]

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Sidebar options for summarization style
    st.sidebar.title("Summary Options")
    summary_option = st.sidebar.radio(
        "Choose how you want to summarize the document:",
        ("Summarize in 100 words", "Summarize in 2 connecting paragraphs", "Summarize in 5 bullet points")
    )

    # Checkbox to select model
    use_advanced_model = st.sidebar.checkbox("Use Advanced Model (gpt-4o)")

    # Choose between 'gpt-4o' and 'gpt-4o-mini'
    model = "gpt-4o" if use_advanced_model else "gpt-4o-mini"

    # Ask the user for a question
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question
        document = uploaded_file.read().decode()

        # Adjust the prompt based on the user's summary option
        if summary_option == "Summarize in 100 words":
            summary_prompt = "Summarize the document in 100 words."
        elif summary_option == "Summarize in 2 connecting paragraphs":
            summary_prompt = "Summarize the document in 2 connecting paragraphs."
        elif summary_option == "Summarize in 5 bullet points":
            summary_prompt = "Summarize the document in 5 bullet points."

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {summary_prompt} {question}",
            }
        ]

        # Generate an answer using the selected OpenAI model
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using st.write_stream
        st.write_stream(stream)
