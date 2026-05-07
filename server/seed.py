import json
from datetime import datetime, timedelta
from db import connect

POSTS = [
    dict(author="Aria", handle="@aria.explores", avatar="🧬", text="Some places don’t feel real. This was one of them.", image_url="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80", tags=["sci-fi art", "worldbuilding"], replies=23, reposts=87, likes=512, source="curated", meaningful_score=70, entertaining_score=58, intellectual_score=62, lighthearted_score=30, original_score=85, viral_score=48, depth_score=72, surface_score=25, positivity_score=78, edgy_score=24, slower_pace_score=80, fast_paced_score=15, niche_score=82, mainstream_score=30),
    dict(author="Thinky Machines", handle="@thinkymachines", avatar="⚙️", text="A short thread on building AI tools that respect your attention instead of stealing it. 🧵 Thread", image_url=None, tags=["AI", "attention", "tools"], replies=17, reposts=64, likes=298, source="following", meaningful_score=92, entertaining_score=35, intellectual_score=88, lighthearted_score=25, original_score=76, viral_score=45, depth_score=90, surface_score=10, positivity_score=70, edgy_score=12, slower_pace_score=78, fast_paced_score=22, niche_score=74, mainstream_score=35),
    dict(author="Lena Park", handle="@lenapark.music", avatar="🎧", text="New ambient track just dropped. Distant Signals — 3:42", image_url=None, tags=["ambient", "music"], replies=12, reposts=45, likes=230, source="small_creators", meaningful_score=55, entertaining_score=70, intellectual_score=38, lighthearted_score=60, original_score=80, viral_score=35, depth_score=50, surface_score=40, positivity_score=84, edgy_score=16, slower_pace_score=88, fast_paced_score=12, niche_score=76, mainstream_score=28),
    dict(author="Civic Static", handle="@civicstatic", avatar="📡", text="The future of cities is not smart sensors everywhere. It is local control over what gets measured and why.", image_url=None, tags=["cities", "governance"], replies=31, reposts=93, likes=420, source="local", meaningful_score=86, entertaining_score=30, intellectual_score=82, lighthearted_score=12, original_score=68, viral_score=42, depth_score=84, surface_score=15, positivity_score=58, edgy_score=30, slower_pace_score=60, fast_paced_score=25, niche_score=70, mainstream_score=40, politics_score=35),
    dict(author="Meme Reactor", handle="@memereactor", avatar="🌀", text="POV: you open your feed for 30 seconds and now you’re angry about six things you didn’t know existed.", image_url=None, tags=["memes"], replies=82, reposts=310, likes=1400, source="curated", meaningful_score=28, entertaining_score=88, intellectual_score=22, lighthearted_score=78, original_score=35, viral_score=92, depth_score=12, surface_score=85, positivity_score=35, edgy_score=55, slower_pace_score=10, fast_paced_score=90, niche_score=20, mainstream_score=90, outrage_score=45, repost_meme_score=90),
    dict(author="Open Garden", handle="@opengarden", avatar="🌱", text="Small communities are not failed mass platforms. They are successful gardens with fences low enough to talk over.", image_url=None, tags=["community", "open web"], replies=9, reposts=51, likes=260, source="small_creators", meaningful_score=88, entertaining_score=42, intellectual_score=75, lighthearted_score=45, original_score=83, viral_score=30, depth_score=78, surface_score=18, positivity_score=90, edgy_score=8, slower_pace_score=84, fast_paced_score=15, niche_score=88, mainstream_score=20),
    dict(author="Viral Forge", handle="@viralforge", avatar="🔥", text="This one trick will completely change how you think about social media algorithms.", image_url=None, tags=["growth"], replies=44, reposts=205, likes=980, source="curated", meaningful_score=38, entertaining_score=75, intellectual_score=35, lighthearted_score=50, original_score=25, viral_score=88, depth_score=20, surface_score=80, positivity_score=48, edgy_score=42, slower_pace_score=18, fast_paced_score=82, niche_score=25, mainstream_score=78, outrage_score=30),
]

def seed_if_empty():
    with connect() as conn:
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        if count:
            return
        now = datetime.utcnow()
        for i, p in enumerate(POSTS):
            p = p.copy()
            p["created_at"] = (now - timedelta(hours=i+2)).isoformat() + "Z"
            p["tags"] = json.dumps(p["tags"])
            columns = ",".join(p.keys())
            placeholders = ",".join(["?"] * len(p))
            conn.execute(f"INSERT INTO posts ({columns}) VALUES ({placeholders})", list(p.values()))
