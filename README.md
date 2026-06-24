# Local SQL Injection Lab

A simple local environment to practice SQL injection safely on your own machine.

## What this setup includes
- A local SQLite database (`database.db`)
- A vulnerable Flask web app (`app.py`)
- A database initializer (`init_db.py`)
- A login form and search form that are intentionally vulnerable to SQL injection

## Requirements
- Python 3.8+ installed locally
- Windows PowerShell or Command Prompt

## Setup steps
1. Open PowerShell in this folder.
2. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Initialize the database:

```powershell
python init_db.py
```

5. Start the app:

```powershell
python app.py
```

6. Open a browser and go to:

- `http://127.0.0.1:5000/login`
- `http://127.0.0.1:5000/search`

### Local network access
If you want to access the app from other devices on the same network, use your PC's local IP address:

- `http://<your-local-ip>:5000/login`
- `http://<your-local-ip>:5000/search`

For example: `http://192.168.1.12:5000/login`

### Deploying on Render with a SQL database
To host this app online for free, use Render for the web app and a free PostgreSQL database service.

1. Push your repository to GitHub, GitLab, or Bitbucket.
2. Sign in to Render and create a new Web Service.
3. Connect your repository and select this project.
4. Use these settings:
   - Environment: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python -m waitress --listen=0.0.0.0:$PORT app:app`

If you prefer Gunicorn, you can try `gunicorn app:app` instead, but Render may work more reliably with `waitress` for this app.

### Create a free PostgreSQL database
- Option 1: Use Render's free PostgreSQL add-on.
- Option 2: Use a free PostgreSQL host like ElephantSQL or Supabase.

Then set this environment variable in Render:

- `DATABASE_URL`

Example value:

`postgres://user:password@hostname:5432/databasename`

### Initialize the database schema manually
You need to create the schema and sample data yourself for your hosted SQL database.

For PostgreSQL, connect to the database and run these commands:

```sql
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES
  ('admin', 'secret123'),
  ('alice', 'alicepass'),
  ('bob', 'bobpass');

INSERT INTO products (name, description) VALUES
  ('Red Shirt', 'A comfortable red shirt'),
  ('Blue Hat', 'A stylish blue hat'),
  ('Coffee Mug', 'A ceramic mug for coffee'),
  ('SQL Book', 'A beginner SQL guide');
```

If you prefer SQLite locally, run:

```powershell
python init_db.py
```

### Notes
- This project is designed for training and is intentionally insecure.
- Keep the hosted app private or temporary.
- Use Render Postgres, ElephantSQL, or Supabase for free SQL hosting.

## How to use
- Login with valid credentials: `admin` / `secret123`
- Search for products using keywords like `shirt`, `hat`, or `coffee`

### Example SQL injection payloads
- Login bypass: `admin' --`
- Search injection: `x' OR '1'='1`

## Safety notice
This environment is intentionally insecure for education only. Do not use these techniques against systems you do not own or have permission to test.
