from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from app.vector_store import get_vector_store_retriever

DB_PATH = "./data/Chinook.sqlite"

def get_db():
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

def get_schema(_):
    db = get_db()
    return db.get_table_info()

def format_docs(docs):
    return "\n\n".join(
        f"User Question: {doc.page_content}\nSQL Query: {doc.metadata['sql_query']}"
        for doc in docs
    )

prompt_template = """You are a SQLite expert. Given a user question, create a syntactically correct SQLite query to run.
Unless the user specifies a specific number of examples to obtain, query for at most 5 results.

You can only use tables provided in the schema below. Do not hallucinate table or column names.
Schema:
{schema}

Here are some examples of user questions and their corresponding SQL queries:
{examples}

User Question: {question}
SQL Query:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

def get_sql_generation_chain():
    retriever = get_vector_store_retriever()
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    chain = (
        RunnablePassthrough.assign(
            schema=get_schema,
            examples=lambda inputs: retriever.get_relevant_documents(inputs["question"])
        )
        | RunnablePassthrough.assign(examples=lambda inputs: format_docs(inputs["examples"]))
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain