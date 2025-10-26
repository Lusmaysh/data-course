import os, psycopg2, psycopg2.extras, logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

def main():
    logging.info("Testing database connection")
    try:
        conn = psycopg2.connect(
            database=db_name, 
            user=db_user, 
            password=db_password, 
            host=db_host, 
            port=db_port
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logging.info("Connected to database successfully")
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise

    try:
        cur.execute("SELECT * FROM vectorizers LIMIT 5")
        rows = cur.fetchall()
        logging.info(f"Query executed successfully, fetched {len(rows)} rows")
        for row in rows:
            print(f"ID: {row['id']}, Params: {row['params']}, Vocabulary: {row['vocabulary']}, IDF: {row['idf']}")
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        raise
    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed")

if __name__ == "__main__":
    main()