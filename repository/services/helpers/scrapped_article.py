from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ScrapedArticle:
    news_id: int
    title: str
    html_content: str
    excerpt: str
    url: str
    published_at: datetime
    updated_at: datetime
    author_name: str
    author_about: str
    source: str
