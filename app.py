import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

class APIAnswer(BaseModel):
    endpoint: str = Field(description="The API endpoint")
    method: str = Field(description="The API method")
    # authentication: str = Field(description="The authentication method")

parser = PydanticOutputParser(pydantic_object=APIAnswer)

documentation = """
Authentication

All requests require Bearer Token.

Endpoint:

POST /users

Headers

Authorization

Content-Type

Request Body

name
email

Returns

201 Created

Errors

400
401
"""

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

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an API Documentation Expert.

Your job is to answer ONLY using the supplied documentation.

If the answer cannot be found in the documentation,
reply with "Not Found".

Always return structured information.

{format_instructions}

Documentation:
{documentation}
"""
        ),
        (
            "human",
            "{question}"
        )
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)

chain = template | model | parser

if st.button("Ask AI"):
    # if not uploaded_file:
    #     st.warning("Please upload a documentation file.")
    if not question:
        st.warning("Please enter a question.")
    else:
        # Read the uploaded file content
        # file_content = uploaded_file.read().decode("utf-8")

        # Invoke the chain with the documentation and question
        result = chain.invoke({
            "documentation": documentation,
            "question": question
        })

        st.subheader("Answer:")
        st.json(result.dict())