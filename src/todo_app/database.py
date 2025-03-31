import sqlite3


class DBHelper:
    def __init__(self, dbname: str):
        self._dbname = dbname
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._dbname)
        self._cursor = self._conn.cursor()
        self._create_table()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self._conn.rollback()
        else:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        self._cursor.execute(query)
        self._conn.commit()

    def add_tasks(self, tasks):
        query = "INSERT INTO todos (task_name, status) VALUES (?, ?)"
        self._cursor.executemany(query, tasks)
        self._conn.commit()

    def remove_task(self, task_id):
        query = f"DELETE FROM todos WHERE id = {task_id}"
        self._cursor.execute(query)
        self._conn.commit()

    def mark_complete(self, task_id):
        query = f"UPDATE todos SET status = 'complete' WHERE id = {task_id}"
        self._cursor.execute(query)
        self._conn.commit()

    def list_tasks(self, filter):
        query = f"SELECT * FROM todos"
        if filter:
            query = f"{query} WHERE status = '{filter}'"
        return self._cursor.execute(query)
