# utils/search.py
# search.py (데이터베이스 호출)
# %% Internal pkgs
from utils.api_keys import openai_api_key
# External pkgs
# from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.retrievers import MultiQueryRetriever
from langchain.chains import RetrievalQA
import logging

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

def chatbot(db_directory : str, question: str) -> None:
    # Load Chroma database
    db = Chroma(persist_directory=db_directory, embedding_function=OpenAIEmbeddings())
    # QA setup
    llm = ChatOpenAI(temperature=0)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(), llm=llm
    )
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    # Process the question
    docs = retriever_from_llm.invoke(input=question)
    for idx, doc in enumerate(docs):
        logger.info(f"[{idx}] Source: {doc.metadata['source']}, Page: {doc.metadata['page']}\nContent: {doc.page_content}")
        src = doc.metadata['source'].split('\\')[-1].split('.')[0]
        content = doc.page_content.replace("\n\n", "\n")
        print(f"#### {idx+1}. {src} | {doc.metadata['page']} 페이지\n{content}")
    result = qa_chain.invoke({"query": question})
    logger.info(f"Q: {result['query']}\nA: {result['result']}")
    print("#### Conclusion\n", result['result'])

def main() -> None:
    while True:
        query = input("Enter query: ")
        if query.lower in ["quit", "break"]:
            break
        chatbot(db_directory="db/chroma_db", question=query)

# Main
if __name__ == '__main__':
    main()
# %%
