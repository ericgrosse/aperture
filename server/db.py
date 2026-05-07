import os, sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DATABASE_PATH", Path(__file__).parent / "aperture.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author TEXT NOT NULL,
  handle TEXT NOT NULL,
  avatar TEXT NOT NULL,
  created_at TEXT NOT NULL,
  text TEXT NOT NULL,
  image_url TEXT,
  tags TEXT NOT NULL,
  replies INTEGER DEFAULT 0,
  reposts INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  source TEXT DEFAULT 'curated',
  meaningful_score INTEGER DEFAULT 50,
  entertaining_score INTEGER DEFAULT 50,
  intellectual_score INTEGER DEFAULT 50,
  lighthearted_score INTEGER DEFAULT 50,
  original_score INTEGER DEFAULT 50,
  viral_score INTEGER DEFAULT 50,
  depth_score INTEGER DEFAULT 50,
  surface_score INTEGER DEFAULT 50,
  positivity_score INTEGER DEFAULT 50,
  edgy_score INTEGER DEFAULT 50,
  slower_pace_score INTEGER DEFAULT 50,
  fast_paced_score INTEGER DEFAULT 50,
  niche_score INTEGER DEFAULT 50,
  mainstream_score INTEGER DEFAULT 50,
  politics_score INTEGER DEFAULT 0,
  outrage_score INTEGER DEFAULT 0,
  repost_meme_score INTEGER DEFAULT 0,
  sensitive_score INTEGER DEFAULT 0
);
"""

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)
