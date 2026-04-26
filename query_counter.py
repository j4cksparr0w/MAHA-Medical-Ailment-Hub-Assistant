from contextlib import contextmanager
from sqlalchemy import event
from db import engine

@contextmanager
def count_queries(capture_sql: bool = False, max_sql: int = 30):
    counter = {"n": 0, "sql": []}

    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        counter["n"] += 1
        if capture_sql and len(counter["sql"]) < max_sql:
            counter["sql"].append(statement)

    event.listen(engine, "before_cursor_execute", before_cursor_execute)
    try:
        yield counter
    finally:
        event.remove(engine, "before_cursor_execute", before_cursor_execute)
