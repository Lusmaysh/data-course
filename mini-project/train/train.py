import os, json, io, hashlib, joblib, psycopg2, psycopg2.extras, logging, sys
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.preprocessing.preprocess import tokenize

load_dotenv()
# print(os.environ["DATABASE_URL"])
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# DATABASE_URL = os.environ["DATABASE_URL"]

def get_conn():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )

def main():
    logging.info("Starting training process")
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logging.info("Connected to database")
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise

    cur.execute("SELECT id, text_raw, label FROM training_samples ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        logging.error("No rows found in training_samples. Seed the DB first.")
        raise RuntimeError("No rows found in training_samples. Seed the DB first.")
    
    texts = [r["text_raw"] for r in rows]
    y = [r["label"] for r in rows]
    logging.info(f"Fetched {len(texts)} training samples")

    Xtr, Xte, ytr, yte = train_test_split(texts, y, test_size=0.33, random_state=42, stratify=y)
    logging.info(f"Split data: {len(Xtr)} train, {len(Xte)} test samples")

    tfidf = TfidfVectorizer(
        tokenizer=tokenize, 
        ngram_range=(1,2), 
        min_df=1, 
        max_df=0.95, 
        lowercase=False
    )
    clf = LinearSVC()
    pipe = Pipeline([("tfidf", tfidf), ("clf", clf)])
    logging.info("Fitting the pipeline")
    pipe.fit(Xtr, ytr)
    logging.info("Pipeline fitted successfully")

    yhat = pipe.predict(Xte)
    logging.info("Predictions made on test set")
    print(classification_report(yte, yhat, digits=3))

    vocab = pipe.named_steps["tfidf"].vocabulary_
    idf   = pipe.named_steps["tfidf"].idf_.tolist()
    params = {"ngram_range": [1,2], "min_df": 1, "max_df": 0.95, "lowercase": False}

    logging.info("Storing vectorizer in database")
    cur.execute(
        """
        INSERT INTO vectorizers 
        (name, params, vocabulary, idf) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id""",
        ("tfidf_v1", json.dumps(params), json.dumps(vocab), json.dumps(idf))
    )
    result = cur.fetchone()
    if result is None:
        logging.error("Failed to insert vectorizer")
        raise RuntimeError("Failed to insert vectorizer")
    
    vectorizer_id = result["id"]
    conn.commit()
    logging.info(f"Vectorizer stored with id {vectorizer_id}")

    buf = io.BytesIO()
    joblib.dump(pipe, buf)
    blob = buf.getvalue()
    sha = hashlib.sha256(blob).hexdigest()
    hyper = {"model": "LinearSVC"}
    metrics = {"n_train": len(Xtr), "n_test": len(Xte)}

    logging.info("Storing model in database")
    cur.execute(
        """
        INSERT INTO models 
        (name, task, vectorizer_id, hyperparams, metrics, artifact, sha256) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        RETURNING id""",
        ("svc_v1", "classification", vectorizer_id, json.dumps(hyper), json.dumps(metrics), blob, sha)
    )
    result = cur.fetchone()
    if result is None:
        logging.error("Failed to insert model")
        raise RuntimeError("Failed to insert model")
    
    model_id = result["id"]
    conn.commit()
    cur.close(); conn.close()
    logging.info(f"Model stored with id {model_id}")
    logging.info("Training process completed successfully")

if __name__ == "__main__":
    main()