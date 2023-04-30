from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI

import requests
import os
from prompt import prompt
from dotenv import load_dotenv

URL = "https://www.dropbox.com/s/9npstuvp2vhnq4z/Untitled%205.pdf?dl=1"
FILE_NAME = "file.pdf"
MAX_TOKENS = 4096


def upload_and_split_text():
    """
    Downloads the PDF file from the URL and splits its content into smaller text chunks.

    Returns:
    A list of smaller text chunks extracted from the PDF file.
    """
    response = requests.get(URL)
    if response.status_code == 200:
        with open(FILE_NAME, "wb") as f:
            f.write(response.content)
    reader = PdfReader(FILE_NAME)
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    text_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(raw_text)


def load_embeddings():
    """
    Loads the OpenAI embeddings and creates a FAISS vector store to search for similar text chunks.

    Returns:
    docsearch: A FAISS vector store.
    chain: A LangChain model for question answering.
    """
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    texts = upload_and_split_text()

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    docsearch = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(
        ChatOpenAI(model_name="gpt-3.5-turbo"), chain_type="stuff", prompt=prompt
    )

    return docsearch, chain


def get_response(message, docsearch, chain):
    """
    Generates a response based on the input message, the docsearch vector store, and the LangChain question answering model.
    Returns:
    A string containing the generated response.
    """
    if len(message) > MAX_TOKENS:
        answer = f"Message exceeds maximum allowed length of {MAX_TOKENS} tokens"
    else:
        docs = docsearch.similarity_search(message)
        answer = chain.run(input_documents=docs, question=message)
    return answer
