from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.pipeline import ask_question
from db import init_db, log_query, get_connection

app = FastAPI(title="NL-to-SQL Analytics Copilot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


class AskRequest(BaseModel):
    question: str


@app.post("/api/ask")
def ask(payload: AskRequest):
    result = ask_question(payload.question)

    if "error" in result:
        log_query(payload.question, result.get("sql"), None)
    else:
        log_query(payload.question, result["sql"], len(result["rows"]))

    return result


@app.get("/api/history")
def get_history():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, question, sql, row_count, created_at FROM query_history ORDER BY created_at DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]





# curl -X POST http://localhost:8000/api/ask \
#   -H "Content-Type: application/json" \
#   -d '{"question": "What are our top 3 customers by total spend?"}'


# curl http://localhost:8000/api/history
