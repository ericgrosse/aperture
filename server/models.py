from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Preferences(BaseModel):
    meaningful: int = 65
    intellectual: int = 65
    original: int = 60
    depth: int = 65
    positivity: int = 80
    slower_pace: int = 65
    niche: int = 65
    politics: str = "show_less"
    outrage: str = "show_less"
    reposts: str = "show_less"
    sensitive: str = "limit"
    sources: Dict[str, int] = Field(default_factory=lambda: {
        "following": 45,
        "curated": 25,
        "small_creators": 20,
        "local": 10,
    })

class PostIn(BaseModel):
    text: str
    author: str = "Nova"
    handle: str = "@novasync"
    image_url: Optional[str] = None
    tags: List[str] = []

class Post(BaseModel):
    id: int
    author: str
    handle: str
    avatar: str
    created_at: str
    text: str
    image_url: Optional[str] = None
    tags: List[str]
    replies: int
    reposts: int
    likes: int
    source: str
    meaningful_score: int
    entertaining_score: int
    intellectual_score: int
    lighthearted_score: int
    original_score: int
    viral_score: int
    depth_score: int
    surface_score: int
    positivity_score: int
    edgy_score: int
    slower_pace_score: int
    fast_paced_score: int
    niche_score: int
    mainstream_score: int
    politics_score: int
    outrage_score: int
    repost_meme_score: int
    sensitive_score: int
    rank_score: Optional[float] = None
    reasons: List[str] = []
