import os

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "admin12345!?")
MYSQL_DB = os.getenv("MYSQL_DB", "hiring_system")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)