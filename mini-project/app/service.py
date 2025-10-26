import os, joblib, psycopg2
import io
from app.preprocessing.preprocess import tokenize
from dotenv import load_dotenv
from threading import Lock

load_dotenv()
_lock = Lock()
_cached_model = None

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def load_latest_model(model_name: str = "svc_v1"):
    global _cached_model

    if _cached_model is not None:
        return _cached_model
    
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT artifact FROM models WHERE name=%s ORDER BY id DESC LIMIT 1",
            (model_name,)
        )
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("No model found. Train and insert a model first.")
        
        blob = row[0].tobytes() if hasattr(row[0], "tobytes") else row[0]
        _cached_model = joblib.load(io.BytesIO(blob))
        return _cached_model