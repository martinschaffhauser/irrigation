import sqlite3


def read_sql_statement(path: str) -> str:
    with open(path, "r") as file:
        sql_statement = file.read()
    return sql_statement


def init_db():
    sql_statement = read_sql_statement("api/operations/sql_statements/init_db.sql")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute(sql_statement)
    conn.commit()
    conn.close()
