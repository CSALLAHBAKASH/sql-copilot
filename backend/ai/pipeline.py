import os
import psycopg2
from ai.schema_introspection import get_connection, get_schema_description, format_schema_for_prompt
from ai.generate_sql import generate_sql
from ai.sql_safety import is_safe_select

from ai.chart_spec import suggest_chart


def _get_readonly_connection():
    return psycopg2.connect(os.getenv("READONLY_DATABASE_URL"))


def ask_question(question: str) -> dict:
    conn = get_connection()
    schema_text = format_schema_for_prompt(get_schema_description(conn))
    conn.close()

    generated = generate_sql(question, schema_text)

    if not is_safe_select(generated.sql):
        return {"error": "Generated query failed safety validation and was not executed.", "sql": generated.sql}

    readonly_conn = _get_readonly_connection()
    cursor = readonly_conn.cursor()
    try:
        cursor.execute(generated.sql)
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        readonly_conn.close()

    # return {"sql": generated.sql, "explanation": generated.explanation, "columns": columns, "rows": rows}
    chart = suggest_chart(columns, rows, question)
    return {
        "sql": generated.sql,
        "explanation": generated.explanation,
        "columns": columns,
        "rows": rows,
        "chart": chart.model_dump(),
    }

if __name__ == "__main__":
    import json

    for question in [
        "What are our top 3 customers by total spend?",
        "How many orders were placed in May 2024?",
    ]:
        result = ask_question(question)
        print(f"\nQ: {question}")
        print(json.dumps(result, indent=2, default=str))