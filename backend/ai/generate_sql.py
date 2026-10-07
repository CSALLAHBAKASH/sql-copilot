import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY is not set — add it to .env")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


class GeneratedQuery(BaseModel):
    sql: str = Field(description="A single, valid PostgreSQL SELECT statement.")
    explanation: str = Field(description="One plain-English sentence describing what the query does.")


generator = llm.with_structured_output(GeneratedQuery)

SQL_PROMPT = """Given this PostgreSQL schema:

{schema}

Write a single SQL query that answers this question: "{question}"

Rules:
- PostgreSQL syntax only.
- SELECT statements only — never modify data.
- Use only the tables and columns shown in the schema above.
- Prefer explicit column names over SELECT *.
"""


def generate_sql(question: str, schema_text: str) -> GeneratedQuery:
    prompt = SQL_PROMPT.format(schema=schema_text, question=question)
    return generator.invoke(prompt)

if __name__ == "__main__":
    from ai.schema_introspection import get_connection, get_schema_description, format_schema_for_prompt

    conn = get_connection()
    schema_text = format_schema_for_prompt(get_schema_description(conn))
    conn.close()

    for question in [
        "What are our top 3 customers by total spend?",
        "How many orders were placed in May 2024?",
        "What's the average order value by product category?",
    ]:
        result = generate_sql(question, schema_text)
        print(f"\nQ: {question}")
        print(f"SQL: {result.sql}")
        print(f"Explanation: {result.explanation}")