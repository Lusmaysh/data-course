CREATE TABLE IF NOT EXISTS documents (
  id           BIGSERIAL PRIMARY KEY,
  source       TEXT,
  created_at   TIMESTAMPTZ DEFAULT now(),
  text_raw     TEXT NOT NULL,
  text_clean   TEXT,
  tokens       JSONB
);

CREATE TABLE IF NOT EXISTS vectorizers (
  id           BIGSERIAL PRIMARY KEY,
  name         TEXT NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT now(),
  params       JSONB NOT NULL,
  vocabulary   JSONB NOT NULL,
  idf          JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS models (
  id           BIGSERIAL PRIMARY KEY,
  name         TEXT NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT now(),
  task         TEXT NOT NULL,
  vectorizer_id BIGINT REFERENCES vectorizers(id) ON DELETE RESTRICT,
  hyperparams  JSONB NOT NULL,
  metrics      JSONB,
  artifact     BYTEA NOT NULL,
  sha256       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS training_samples (
  id BIGSERIAL PRIMARY KEY,
  text_raw TEXT NOT NULL,
  label TEXT NOT NULL
);

-- Useful indexes
CREATE INDEX ON documents USING GIN (tokens jsonb_path_ops);
CREATE INDEX ON models (name);
CREATE INDEX ON vectorizers (name);