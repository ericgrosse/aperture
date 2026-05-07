from models import Preferences

PAIRS = [
    ("meaningful", "meaningful_score", "entertaining_score"),
    ("intellectual", "intellectual_score", "lighthearted_score"),
    ("original", "original_score", "viral_score"),
    ("depth", "depth_score", "surface_score"),
    ("positivity", "positivity_score", "edgy_score"),
    ("slower_pace", "slower_pace_score", "fast_paced_score"),
    ("niche", "niche_score", "mainstream_score"),
]

LABELS = {
    "meaningful": "meaningful content", "intellectual": "intellectual posts", "original": "original creators",
    "depth": "deeper discussion", "positivity": "positive interactions", "slower_pace": "a slower feed pace", "niche": "niche discovery",
}

def penalty(value: int, mode: str) -> float:
    if mode in ("show_less", "limit"):
        return -0.35 * value
    if mode == "show_more":
        return 0.15 * value
    return 0

def rank_post(post: dict, prefs: Preferences) -> dict:
    score = 0.0
    reasons = []
    for pref_name, left_key, right_key in PAIRS:
        pref = getattr(prefs, pref_name)
        left_weight = pref / 100
        right_weight = 1 - left_weight
        contribution = post[left_key] * left_weight + post[right_key] * right_weight
        score += contribution
        if pref >= 60 and post[left_key] >= 70:
            reasons.append(f"Matches your preference for {LABELS[pref_name]}")
        elif pref <= 40 and post[right_key] >= 70:
            reasons.append(f"Matches your preference for {right_key.replace('_score', '').replace('_', ' ')}")

    source_mix = prefs.sources or {}
    source_bonus = source_mix.get(post.get("source", "curated"), 20) * 0.6
    score += source_bonus
    if source_bonus >= 18:
        reasons.append(f"Boosted by your {post.get('source', 'curated').replace('_', ' ')} source mix")

    score += penalty(post.get("politics_score", 0), prefs.politics)
    score += penalty(post.get("outrage_score", 0), prefs.outrage)
    score += penalty(post.get("repost_meme_score", 0), prefs.reposts)
    score += penalty(post.get("sensitive_score", 0), prefs.sensitive)

    if prefs.outrage == "show_less" and post.get("outrage_score", 0) < 20:
        reasons.append("Low ragebait score")
    if prefs.reposts == "show_less" and post.get("repost_meme_score", 0) < 25:
        reasons.append("Prioritized over repost-heavy content")

    post["rank_score"] = round(score, 2)
    post["reasons"] = reasons[:4] or ["Balanced match for your current settings"]
    return post

def rank_posts(posts: list[dict], prefs: Preferences) -> list[dict]:
    return sorted([rank_post(dict(p), prefs) for p in posts], key=lambda p: p["rank_score"], reverse=True)
