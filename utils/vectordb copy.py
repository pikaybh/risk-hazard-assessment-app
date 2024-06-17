import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List
import logging

# Logger setup
logger_name = 'vectordb'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'))
logger.addHandler(file_handler)

# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)

# Function to get all PDF files in a directory
def get_pdf_files(root_dir: str) -> List[str]:
    """
    Recursively searches for PDF files in the given directory.

    :param root_dir: The root directory to search for PDF files.
    :type root_dir: str
    :return: A list of paths to the PDF files found.
    :rtype: List[str]
    """
    pdf_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(dirpath, filename))
    logger.info(f"Found {len(pdf_files)} PDF files in {root_dir}")
    return pdf_files

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Function to convert PDFs to vector database
def pdfs_to_vectordb(pdf_files: List[str], db_path: str) -> None:
    texts = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        if text.strip():  # Ensure text is not empty or whitespace
            texts.append(text)
        else:
            logger.warning(f"No text found in {pdf_file}")

    if not texts:
        logger.error("No text found in any of the PDF files.")
        raise ValueError("No text found in any of the PDF files.")

    # Use SentenceTransformers to embed the texts
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)

    # Initialize FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, db_path)
    logger.info(f"Vector database saved to {db_path}")

    # Save metadata (filenames)
    metadata_path = db_path.replace('.faiss', '_metadata.txt')
    with open(metadata_path, 'w', encoding='utf-8-sig') as f:
        for pdf_file in pdf_files:
            f.write(f"{pdf_file}\n")
    logger.info(f"Metadata saved to {metadata_path}")

def main() -> None:
    # Set the directory for PDF files and the path for the vector database
    pdf_files = get_pdf_files("src")  # Add the path to the PDF files
    db_path = "db/vectordb.faiss"

    # Convert PDF files to vector database
    pdfs_to_vectordb(pdf_files, db_path)

# Main
if __name__ == '__main__':
    main()
