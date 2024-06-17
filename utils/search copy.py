# utils/search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util
import logging
from PyPDF2 import PdfReader
from tqdm import tqdm

# Logger setup
logger_name = 'search'
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

class VectorDBSearcher:
    def __init__(self, db_path: str, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the searcher with the vector database path and the embedding model.
        
        :param db_path: Path to the FAISS vector database.
        :param model_name: Name of the SentenceTransformer model to use for embeddings.
        """
        self.db_path = db_path
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(db_path)
        self.filenames = []
        self.load_metadata()

    def load_metadata(self):
        """
        Load metadata (filenames) from the vector database if stored separately.
        """
        try:
            metadata_path = self.db_path.replace('.faiss', '_metadata.txt')
            with open(metadata_path, 'r', encoding='utf-8-sig') as f:
                self.filenames = [line.strip() for line in f]
            logger.info(f"Loaded metadata from {metadata_path}")
        except FileNotFoundError:
            logger.error("Metadata file not found. Continuing without filenames.")

    def search(self, query: str, top_k: int = 5):
        """
        Search for the top_k most relevant entries in the vector database for the given query.
        
        :param query: The query string to search for.
        :param top_k: Number of top results to return.
        :return: List of tuples (filename, score)
        """
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.filenames):
                results.append((self.filenames[idx], dist))
            else:
                results.append(("Unknown file", dist))
        
        return results

    def extract_similar_texts(self, filename: str, query: str, top_k: int = 5):
        """
        Extract similar texts from a given file based on the query.
        
        :param filename: The filename to extract texts from.
        :param query: The query string to search for.
        :param top_k: Number of top results to return.
        :return: List of tuples (text, score)
        """
        # Extract text from the PDF file
        reader = PdfReader(filename)
        content = ""
        for page in reader.pages:
            content += page.extract_text() + "\n"

        sentences = content.split('\n')
        sentence_embeddings = self.model.encode(sentences)
        query_embedding = self.model.encode([query])

        # Calculate cosine similarities
        similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
        top_results = similarities.topk(top_k)

        similar_texts = []
        for score, idx in zip(top_results[0], top_results[1]):
            similar_texts.append((sentences[idx], score.item()))

        return similar_texts

if __name__ == '__main__':
    searcher = VectorDBSearcher('db/vectordb.faiss')
    query = input("Enter your query: ")
    results = searcher.search(query)

    logger.info("\nSearch Results:")
    for filename, score in results:
        logger.info(f"File: {filename}, Score: {score}")
        similar_texts = searcher.extract_similar_texts(filename, query)
        logger.info("Similar texts:")
        for text, text_score in similar_texts:
            logger.info(f" - {text}, Score: {text_score}")

    # Show progress using tqdm
    logger.info("\nProcessing similar texts...")
    for filename, score in tqdm(results, desc="Processing files"):
        logger.info(f"\nProcessing file: {filename}")
        similar_texts = searcher.extract_similar_texts(filename, query)
        logger.info("Similar texts:")
        for text, text_score in similar_texts:
            logger.info(f" - {text}, Score: {text_score}")
