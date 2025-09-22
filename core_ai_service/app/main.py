from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from app.chain import get_sql_generation_chain
from app.schemas import SQLQueryRequest, SQLQueryResponse

load_dotenv(dotenv_path="../.env")

app = FastAPI(
    title="Text-to-SQL Core AI Service",
    description="A service to convert natural language questions into SQL queries.",
)

sql_chain = get_sql_generation_chain()

@app.post("/generate-sql", response_model=SQLQueryResponse)
async def generate_sql(request: SQLQueryRequest):
    try:
        result = sql_chain.invoke({"question": request.question})
        return SQLQueryResponse(sql_query=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))