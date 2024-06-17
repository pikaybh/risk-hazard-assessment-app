# vectordb.py
# %% Internal pkgs
from utils.api_keys import openai_api_key
# External pkgs
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
import os
import logging

# Logger setup
logger_name = 'vectordb'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname): %(message)s'))
logger.addHandler(file_handler)
# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)

# Function to load and split all PDFs in a directory
def load_and_split_pdfs(directory : str) -> tuple:
    all_texts : list = []
    metadata : list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                logger.info(f"Processing file: {file_path}")
                try:
                    pages = PyPDFLoader(file_path).load_and_split()
                    texts = RecursiveCharacterTextSplitter(
                        chunk_size=300,
                        chunk_overlap=20,
                        length_function=len,
                        is_separator_regex=False,
                    ).split_documents(pages)
                    all_texts.extend(texts)
                    for idx, text in enumerate(texts):
                        metadata.append({"source": file_path, "page": idx + 1})
                    logger.info(f"Loaded and split {len(texts)} documents from {file_path}")
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {e}")
    return all_texts, metadata

"""
# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
"""

def to_db(pdf_directory : str) -> Chroma:
    # Load and split PDFs
    texts, metadata = load_and_split_pdfs(pdf_directory)
    # Load it into Chroma
    return Chroma.from_texts(
        texts=[text.page_content for text in texts], 
        embedding=OpenAIEmbeddings(), 
        persist_directory="db/chroma_db", 
        metadatas=metadata
    ).persist()

def main() -> None:
    to_db(r"src\법규")

# Main
if __name__ == '__main__':
    main()
# %%
