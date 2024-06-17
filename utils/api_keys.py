import os
from dotenv import load_dotenv


load_dotenv(verbose=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")