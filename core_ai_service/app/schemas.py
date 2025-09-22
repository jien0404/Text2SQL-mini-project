from pydantic import BaseModel

class SQLQueryRequest(BaseModel):
    question: str

class SQLQueryResponse(BaseModel):
    sql_query: str
    error: str | None = None