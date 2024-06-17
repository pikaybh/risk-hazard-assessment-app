# Internal Modules
import utils
from utils import (vectordb, search)
# External Modules
import chardet
import logging
import argparse

# Root 
logger_name = '__main__'
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
# Argparse
parser : argparse.ArgumentParser = argparse.ArgumentParser(description=...)
parser.add_argument('--vectorize', '-V', default=None, type=str, help=...)
parser.add_argument('--search', '-S', default=None, type=str, help=...)
parser.add_argument('--source', '-C', default=None, type=str, help=...)
args : argparse.Namespace = parser.parse_args()

# main
def main() -> None:
    if args.vectorize:
        # Set the directory for PDF files and the path for the vector database
        pdf_files = vectordb.get_pdf_files("src")  # Add the path to the PDF files
        db_path = "db/vectordb.faiss"

        # Convert PDF files to vector database
        vectordb.pdfs_to_vectordb(pdf_files, db_path)

    if args.search:
        searcher = search.VectorDBSearcher('db/vectordb.faiss')
        results = searcher.search(args.search)

        logger.info("\nSearch Results:")
        for filename, score in results:
            logger.info(f"File: {filename}, Score: {score}")
            similar_texts = searcher.extract_similar_texts(filename, args.search)
            logger.info("Similar texts:")
            for text, text_score in similar_texts:
                logger.info(f" - {text}, Score: {text_score}")

        # Show progress using tqdm
        logger.info("\nProcessing similar texts...")
        for filename, score in tqdm(results, desc="Processing files"):
            logger.info(f"\nProcessing file: {filename}")
            similar_texts = searcher.extract_similar_texts(filename, args.search)
            logger.info("Similar texts:")
            for text, text_score in similar_texts:
                logger.info(f" - {text}, Score: {text_score}")

    if args.source:
        df : pd.DataFrame = get_df(r"docs\codenaming.xlsx")

def cal():
    print(f"{9_113_333 + 2 * 5_240_988 + 2 * 1_062_701 + 2_400_516:,}")

# Main
if __name__ == '__main__':
    main()
