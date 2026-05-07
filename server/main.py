import json, os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, connect
from seed import seed_if_empty
from models import Preferences, PostIn
from ranking import rank_posts

app = FastAPI(title="Aperture API")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    seed_if_empty()

def rows_to_posts(rows):
    posts = []
    for row in rows:
        d = dict(row)
        d["tags"] = json.loads(d["tags"] or "[]")
        posts.append(d)
    return posts

@app.get("/api/health")
def health():
    return {"ok": True, "app": "Aperture"}

@app.get("/api/posts")
def get_posts():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return rows_to_posts(rows)

@app.post("/api/feed/rank")
def rank_feed(prefs: Preferences):
    with connect() as conn:
        rows = conn.execute("SELECT * FROM posts").fetchall()
    return {"posts": rank_posts(rows_to_posts(rows), prefs)}

@app.post("/api/posts")
def create_post(post: PostIn):
    text = post.text.strip()

    if not text:
        return {"error": "Post text cannot be empty"}

    lowered = text.lower()

    meaningful = 75 if len(text) > 120 else 55
    intellectual = 75 if any(w in lowered for w in ["algorithm", "system", "ai", "internet", "future", "social", "feed"]) else 50
    original = 80
    depth = 70 if len(text) > 160 else 52
    positivity = 72 if not any(w in lowered for w in ["rage", "doom", "hate", "angry"]) else 45
    edgy = 35 if positivity >= 60 else 65
    niche = 70 if any(w in lowered for w in ["cyberpunk", "algorithm", "aperture", "decentralized", "open web"]) else 50

    tags = post.tags or ["user post"]

    with connect() as conn:
        cur = conn.execute("""
        INSERT INTO posts (
            author, handle, avatar, created_at, text, image_url, tags,
            replies, reposts, likes, source,
            meaningful_score, entertaining_score,
            intellectual_score, lighthearted_score,
            original_score, viral_score,
            depth_score, surface_score,
            positivity_score, edgy_score,
            slower_pace_score, fast_paced_score,
            niche_score, mainstream_score,
            politics_score, outrage_score, repost_meme_score, sensitive_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 'following',
            ?, 45,
            ?, 35,
            ?, 25,
            ?, 35,
            ?, ?,
            65, 30,
            ?, 35,
            0, 0, 0, 0
        )
        """, (
            post.author,
            post.handle,
            "🧠",
            datetime.utcnow().isoformat() + "Z",
            text,
            post.image_url,
            json.dumps(tags),
            meaningful,
            intellectual,
            original,
            depth,
            positivity,
            edgy,
            niche,
        ))

        conn.commit()
        row = conn.execute("SELECT * FROM posts WHERE id = ?", (cur.lastrowid,)).fetchone()

    return rows_to_posts([row])[0]

@app.get("/api/modes")
def modes():
    return {
        "Default": {"meaningful":55,"intellectual":55,"original":55,"depth":55,"positivity":60,"slower_pace":50,"niche":50},
        "Deep Focus": {"meaningful":82,"intellectual":80,"original":72,"depth":86,"positivity":72,"slower_pace":82,"niche":68},
        "Creative Spark": {"meaningful":65,"intellectual":55,"original":88,"depth":60,"positivity":78,"slower_pace":58,"niche":82},
        "Local Pulse": {"meaningful":72,"intellectual":58,"original":70,"depth":65,"positivity":75,"slower_pace":60,"niche":74,"sources":{"following":25,"curated":15,"small_creators":20,"local":40}},
        "Custom Mode": {}
    }
