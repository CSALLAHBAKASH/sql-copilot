import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def get_schema_description(connection) -> dict:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """)
    schema: dict = {}
    for table_name, column_name, data_type in cursor.fetchall():
        schema.setdefault(table_name, []).append({"column_name": column_name, "data_type": data_type})
    cursor.close()
    return schema

def format_schema_for_prompt(schema: dict) -> str:
    lines = []
    for table_name, columns in schema.items():
        column_list = ", ".join(f"{c['column_name']} {c['data_type']}" for c in columns)
        lines.append(f"{table_name}({column_list})")
    return "\n".join(lines)


if __name__ == "__main__":
    conn = get_connection()
    schema = get_schema_description(conn)
    print(format_schema_for_prompt(schema))
    conn.close()