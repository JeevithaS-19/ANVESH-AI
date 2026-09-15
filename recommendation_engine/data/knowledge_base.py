import json
import os

import pg8000
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "anvesh_prototype")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

PG_CONFIG = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "database": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}

if POSTGRES_HOST not in ("localhost", "127.0.0.1"):
    PG_CONFIG["ssl_context"] = True