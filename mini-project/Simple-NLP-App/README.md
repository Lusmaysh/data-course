# Minimal NLP + FastAPI + Postgres (TF-IDF + LinearSVC)

This is a simple NLP application that uses TF-IDF vectorization and a LinearSVC classifier for text classification (e.g., sentiment analysis). It includes a FastAPI backend, PostgreSQL for storage, and training scripts. The app preprocesses text using spaCy, trains on a small dataset, and serves predictions via an API.

## Prerequisites

- Python 3.8+
- PostgreSQL (for native setup)
- Docker and Docker Compose (for containerized setup)
- Git (to clone the repo if needed)

## Setup

Choose one of the following setup options based on your environment.

### Option 1: Using Native Python and PostgreSQL Server

1. **Install Dependencies**:
  Open a terminal/PowerShell and run:
   - Ensure Python 3.8+ is installed.
     ```bash
      python --version
    ```
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Download the spaCy language model:
     ```bash
     python -m spacy download en_core_web_sm
     ```

2. **Set Up PostgreSQL**:
   - Install and start PostgreSQL on your system (e.g., via Homebrew on macOS, apt on Ubuntu, or official installer).
   - Create a database named `nlpdb` (or choose a different name and update the connection string accordingly).
   - Create a user (e.g., `app`) with a password (e.g., `secret`) and grant permissions on the database.
   - Example commands (run as PostgreSQL superuser):
     ```sql
     CREATE DATABASE nlpdb;
     CREATE USER app WITH PASSWORD 'secret';
     GRANT ALL PRIVILEGES ON DATABASE nlpdb TO app;
     ```
   - Ensure the `app` user can connect and has the necessary privileges to manipulate the database.

3. **Configure Environment**:
   - Create a `.env` file or rename the example `.env.example` to `.env` in the project root with your database connection:
     ```
     DATABASE_URL=postgresql://app:secret@localhost:5432/nlpdb
     ```
     or
     Adjust the URL if your host, port, user, password, or database name differ.
     ```
     DB_HOST=localhost
     DB_PORT=5432
     DB_USER=app
     DB_PASSWORD=secret
     DB_NAME=nlpdb
     ```

4. **Initialize the Database**:
   - Run the schema and seed scripts using psql or a similar tool:
     ```
     psql $DATABASE_URL -f initdb/001_schema.sql
     psql $DATABASE_URL -f initdb/010_seed.sql
     ```
     Replace $DATABASE_URL` with your actual connection string if not set as an environment variable.
     
     or

     Copy-paste the SQL commands in `initdb/001_schema.sql` and `initdb/010_seed.sql` into your PostgreSQL client and execute them.

5. **Train the Model**:
   - Run the training script to train the model and store artifacts in the database:
     ```bash
     python train/train.py
     ```

6. **Start the API**:
   - Launch the FastAPI server:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
     ```

7. **Test the API**:
   - Use curl or a tool like Postman to test predictions:
     ```bash
     curl -X POST http://localhost:8000/predict \
       -H "Content-Type: application/json" \
       -d '{"text": "The ramen was great!"}'
     ```
     Expected response: JSON with `label` (e.g., "pos") and optional `proba`.

### Option 2: Using Docker (Containerized Environment)

1. **Build and Start Services**:
   - Ensure Docker and Docker Compose are installed.
   - Start the PostgreSQL database:
     ```bash
     docker compose up -d --build db
     ```
     This initializes the database with the schema and seed data from `initdb/`.

2. **Train the Model**:
   - Run the training script inside the API container (after the DB is ready):
     ```bash
     docker compose run --rm api python train/train.py
     ```
     This trains the model and stores artifacts in the database.

3. **Start the API**:
   - Launch the API service:
     ```bash
     docker compose up -d api
     ```

4. **Test the API**:
   - Test predictions as in Option 1:
     ```bash
     curl -X POST http://localhost:8000/predict \
       -H "Content-Type: application/json" \
       -d '{"text": "The ramen was great!"}'
     ```

5. **Stop Services**:
   - To stop and clean up:
     ```bash
     docker compose down -v
     ```

## API Endpoints

- `GET /health`: Health check (returns `{"status": "ok"}`).
- `POST /predict`: Predict sentiment for input text. Body: `{"text": "your text here"}`. Response: `{"label": "pos" or "neg", "proba": 0.95}` (proba is optional).

## Notes

- Artifacts (vectorizer params/vocab/idf + model blob) are stored in PostgreSQL.
- You can extend the schema with prediction logs or add pgvector later for embeddings.
- Replace the tiny seed dataset by inserting your own rows into `training_samples`.
- For production, consider adding authentication, rate limiting, and logging.
- If you encounter issues, ensure the spaCy model is downloaded and the database is accessible.