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

### Deploying on Render
To host this app on Render:

1. Create a Git repository in this folder and push it to GitHub, GitLab, or Bitbucket.
2. Sign in to Render and create a new Web Service.
3. Connect your repository.
4. Use these settings:
   - Environment: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

Render sets the `PORT` environment variable automatically, so the app will bind correctly.

> Important: this app is intentionally insecure. Only deploy it to a private or temporary service for learning, not for production or public exposure.

If you need temporary public access for a demo, use a tunnel service like `ngrok` or `localtunnel`, but keep the app offline when you're not using it.

## How to use
- Login with valid credentials: `admin` / `secret123`
- Search for products using keywords like `shirt`, `hat`, or `coffee`

### Example SQL injection payloads
- Login bypass: `admin' --`
- Search injection: `x' OR '1'='1`

## Safety notice
This environment is intentionally insecure for education only. Do not use these techniques against systems you do not own or have permission to test.
