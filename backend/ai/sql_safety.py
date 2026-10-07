import sqlparse
from sqlparse.sql import Statement
from sqlparse.tokens import DML, DDL

FORBIDDEN_KEYWORDS = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT"}


def is_safe_select(sql: str) -> bool:
    statements = sqlparse.parse(sql)
    if len(statements) != 1:
        return False  # reject multi-statement input outright — a classic injection vector

    statement: Statement = statements[0]
    tokens = [t for t in statement.flatten() if not t.is_whitespace]
    if not tokens or tokens[0].ttype is not DML or tokens[0].value.upper() != "SELECT":
        return False

    for token in tokens:
        if token.ttype in (DML, DDL) and token.value.upper() in FORBIDDEN_KEYWORDS:
            return False

    return True


if __name__ == "__main__":
    print(is_safe_select("SELECT * FROM orders"))                                  # True
    print(is_safe_select("SELECT * FROM orders; DROP TABLE orders;"))              # False
    print(is_safe_select("UPDATE orders SET quantity = 0"))                        # False
    print(is_safe_select("SELECT * FROM orders WHERE id IN (DELETE FROM x)"))      # False