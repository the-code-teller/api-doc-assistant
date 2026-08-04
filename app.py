import streamlit as st

st.set_page_config(
    page_title="API Documentation Assistant",
    page_icon="📘",
    layout="wide"
)

st.title("📘 API Documentation Assistant")

st.markdown(
    """
Upload your API documentation and ask questions in natural language.
"""
)

uploaded_file = st.file_uploader(
    "Upload Documentation",
    type=["pdf", "json", "yaml", "yml"]
)

question = st.text_input(
    "Ask a question",
    placeholder="Example: How do I authenticate?"
)

if st.button("Ask AI"):

    if uploaded_file is None:
        st.warning("Please upload a document.")
    elif question.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.success("Everything looks good! AI integration coming next.")