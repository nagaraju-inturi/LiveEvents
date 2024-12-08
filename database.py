import sqlite3

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if self.conn is None:
            self.connect()
        if params:
            return self.conn.execute(query, params)
        else:
            return self.conn.execute(query)
    def update_record(self, table_name, column_name, new_value, where_clause):
        try:
            query = f"UPDATE {table_name} SET {column_name} = ? WHERE {where_clause}"
            self.cursor.execute(query, (new_value,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False
        
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

if __name__ == '__main__':
    # Example usage:
    db = Database("mydatabase.db")
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("delete from users")
    db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    db.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    success = db.update_record("users", "name", "Sam", "id = 2")
    if success:
        print("Record updated successfully!")
    db.conn.commit()

    for row in db.execute("SELECT * FROM users"):
        print(row)

    db.close()