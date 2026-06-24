import os
import sqlite3

try:
    import psycopg2
except ImportError:
    psycopg2 = None

DB_FILE = os.environ.get('SQLITE_DB', 'database.db')
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
USE_POSTGRES = bool(DATABASE_URL)


def get_db_connection():
    if USE_POSTGRES:
        if psycopg2 is None:
            raise RuntimeError('psycopg2 is required for PostgreSQL support')
        return psycopg2.connect(DATABASE_URL, sslmode='require')

    return sqlite3.connect(DB_FILE)


def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS products')
        cursor.execute('''
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        cursor.executemany(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            [
                ('admin', 'secret123'),
                ('alice', 'alicepass'),
                ('bob', 'bobpass'),
            ]
        )
        cursor.executemany(
            'INSERT INTO products (name, description) VALUES (%s, %s)',
            [
                ('Red Shirt', 'A comfortable red shirt'),
                ('Blue Hat', 'A stylish blue hat'),
                ('Coffee Mug', 'A ceramic mug for coffee'),
                ('SQL Book', 'A beginner SQL guide'),
            ]
        )
    else:
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

    target = DATABASE_URL if USE_POSTGRES else DB_FILE
    print(f'Database created: {target}')


if __name__ == '__main__':
    create_database()
