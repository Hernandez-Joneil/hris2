# HRIS2

HRIS2 is a Flask-based hiring and applicant tracking system with applicant exam scheduling, application review, and status tracking.

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a local `config.py` file if it does not exist.
   ```python
   import os

   MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
   MYSQL_USER = os.getenv('MYSQL_USER', 'root')
   MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'admin12345!?')
   MYSQL_DB = os.getenv('MYSQL_DB', 'hiring_system')
   UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

   if not os.path.exists(UPLOAD_FOLDER):
       os.makedirs(UPLOAD_FOLDER)
   ```
4. Set environment variables for production or Render with actual database values:
   - `MYSQL_HOST` = your MySQL host
   - `MYSQL_USER` = your database user
   - `MYSQL_PASSWORD` = your database password
   - `MYSQL_DB` = your database name
   - `SECRET_KEY` = a random session secret
   - `UPLOAD_FOLDER` = `uploads` (optional)

   Do not leave `MYSQL_HOST` as `your_mysql_host`.

5. Run locally:
   ```bash
   python app.py
   ```

## GitHub / Render Deployment

- Create a fresh GitHub repository named `hris2`.
- Add this repo as the new remote and push:
  ```bash
  git remote remove origin
  git remote add origin https://github.com/<username>/hris2.git
  git branch -M main
  git add .
  git commit -m "Initialize HRIS2 deployment-ready project"
  git push -u origin main
  ```

- On Render, create a new Web Service with:
  - Environment: Python
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`
  - Set environment variables in Render dashboard for MySQL and `SECRET_KEY`
