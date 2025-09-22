from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vector_store_retriever():
    persist_directory = "chroma_db_fs"
    embeddings = OpenAIEmbeddings()
    vector_db = Chroma(
        persist_directory=persist_directory, 
        embedding_function=embeddings
    )
    return vector_db.as_retriever()