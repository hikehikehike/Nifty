from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import requests
import os
from apikey import apikey
from prompt import prompt

URL = "https://www.dropbox.com/s/9npstuvp2vhnq4z/Untitled%205.pdf?dl=1"
FILE_NAME = "file.pdf"


def upload_and_split_text():
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
    os.environ["OPENAI_API_KEY"] = apikey

    texts = upload_and_split_text()

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(OpenAI(), chain_type="stuff", prompt=prompt)

    return docsearch, chain


def get_response(message, docsearch, chain):
    docs = docsearch.similarity_search(message)
    answer = chain.run(input_documents=docs, question=message)
    return answer
