import os
from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

DB_FILE = os.environ.get('SQLITE_DB', 'database.db')
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
USE_POSTGRES = bool(DATABASE_URL)

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

app = Flask(__name__)

HTML_LOGIN = '''
<h1>Vulnerable Login</h1>
<form method="post">
  Username: <input name="username" value="admin"><br>
  Password: <input name="password"><br>
  <button type="submit">Login</button>
</form>
<p>{{ message }}</p>
<p>Try SQL injection: <code>admin' --</code></p>
''' 

HTML_SEARCH = '''
<h1>Vulnerable Search</h1>
<form method="get">
  Search: <input name="q" value="coffee"><br>
  <button type="submit">Search</button>
</form>
<ul>
{% for row in rows %}
  <li><strong>{{ row['name'] }}</strong>: {{ row['description'] }}</li>
{% endfor %}
</ul>
<p>{{ message }}</p>
<p>Try SQL injection: <code>x' OR '1'='1</code></p>
'''


def get_db_connection():
    if USE_POSTGRES:
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except Exception as exc:
            raise RuntimeError(f'PostgreSQL import failure: {exc}') from exc

        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Vulnerable SQL string concatenation
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = None
        user = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
        except Exception as error:
            message = f'Error: {error}'
        finally:
            if conn is not None:
                conn.close()

        if user:
            return render_template_string('<h1>Welcome, {{ user }}</h1><p>Login successful.</p>', user=user['username'])
        if not message:
            message = 'Invalid credentials.'

    return render_template_string(HTML_LOGIN, message=message)

@app.route('/search')
def search():
    message = ''
    rows = []
    query = request.args.get('q', '').strip()
    if query:
        # Vulnerable query construction
        sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%';"
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                message = 'No results found.'
        except Exception as error:
            message = f'Error: {error}'
        finally:
            if conn is not None:
                conn.close()

    return render_template_string(HTML_SEARCH, rows=rows, message=message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
