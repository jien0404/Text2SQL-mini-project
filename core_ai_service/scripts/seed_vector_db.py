from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

import os
import sys

# Add the parent directory to the sys.path to allow imports from the 'app' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

# This is a one-time setup script
# In a real application, you might load these from a file or database

FEW_SHOT_EXAMPLES = [
    {
        "input": "How many employees are there?",
        "query": "SELECT count(*) FROM Employee;"
    },
    {
        "input": "List all artists.",
        "query": "SELECT Name FROM Artist;"
    },
    {
        "input": "Who are the employees who are sales support agents?",
        "query": "SELECT * FROM Employee WHERE Title = 'Sales Support Agent';"
    },
    {
        "input": "Show the total sales for each country.",
        "query": "SELECT BillingCountry, SUM(Total) AS TotalSales FROM Invoice GROUP BY BillingCountry ORDER BY TotalSales DESC;"
    },
    {
        "input": "Which artist has the most albums?",
        "query": "SELECT T2.Name, count(T1.AlbumId) AS TotalAlbums FROM Album AS T1 INNER JOIN Artist AS T2 ON T1.ArtistId = T2.ArtistId GROUP BY T2.Name ORDER BY TotalAlbums DESC LIMIT 1;"
    },
    {
        "input": "What is the total revenue for the year 2010?",
        "query": "SELECT SUM(Total) FROM Invoice WHERE strftime('%Y', InvoiceDate) = '2010';"
    },
    {
        "input": "List the top 5 selling tracks.",
        "query": "SELECT T2.Name, sum(T1.UnitPrice * T1.Quantity) AS Revenue FROM InvoiceLine AS T1 INNER JOIN Track AS T2 ON T1.TrackId = T2.TrackId GROUP BY T2.Name ORDER BY Revenue DESC LIMIT 5;"
    }
]

def seed_database():
    print("Seeding vector database with few-shot examples...")
    
    # Use the same Chroma directory that the main app will use
    persist_directory = "chroma_db_fs"
    
    # Check if the database already exists to avoid re-seeding
    if os.path.exists(persist_directory):
        print("Vector database already exists. Skipping seeding.")
        return

    embeddings = OpenAIEmbeddings()
    
    # Prepare documents for ChromaDB
    # We store the SQL query in the metadata
    docs = [
        Document(
            page_content=example["input"],
            metadata={"sql_query": example["query"]}
        )
        for example in FEW_SHOT_EXAMPLES
    ]

    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Successfully seeded vector database at '{persist_directory}'")

if __name__ == "__main__":
    seed_database()