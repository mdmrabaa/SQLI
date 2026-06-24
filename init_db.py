import sqlite3

DB_FILE = 'database.db'

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    cursor.executemany(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        [
            ('admin', 'secret123'),
            ('alice', 'alicepass'),
            ('bob', 'bobpass'),
        ]
    )

    cursor.executemany(
        'INSERT INTO products (name, description) VALUES (?, ?)',
        [
            ('Red Shirt', 'A comfortable red shirt'),
            ('Blue Hat', 'A stylish blue hat'),
            ('Coffee Mug', 'A ceramic mug for coffee'),
            ('SQL Book', 'A beginner SQL guide'),
        ]
    )

    conn.commit()
    conn.close()
    print(f'Database created: {DB_FILE}')

if __name__ == '__main__':
    create_database()
