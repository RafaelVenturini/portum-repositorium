import json
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from repository.ext.db import db
from repository.models import Articles, Authors

PORTO_CENTRAL_POSTS_URL = "https://www.portocentral.com.br/wp-json/wp/v2/posts"
PORTO_CENTRAL_SOURCE_NAME = "Porto Central"


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.parts.append(value)

    def text(self):
        return " ".join(self.parts)


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


def fetch_porto_central_posts(limit=5, page=1, order="desc"):
    params = {
        "per_page": limit,
        "page": page,
        "orderby": "date",
        "order": order,
        "_embed": "1",
    }
    url = f"{PORTO_CENTRAL_POSTS_URL}?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "Chrome/124.0 Safari/537.36"
            ),
        },
    )

    with urlopen(request, timeout=30) as response:
        return json.load(response)


def scrape_porto_central(limit=5, page=1, order="desc") -> list[ScrapedArticle]:
    posts = fetch_porto_central_posts(limit=limit, page=page, order=order)
    return [parse_post(post) for post in posts]


def save_articles(articles: Iterable[ScrapedArticle]) -> tuple[int, int]:
    created = 0
    updated = 0
    now = datetime.utcnow()

    for item in articles:
        author = _get_or_create_author(item, now)
        article = Articles.query.filter_by(news_id=item.news_id).first()

        if article is None:
            article = Articles(
                news_id=item.news_id,
                title=item.title,
                html_content=item.html_content,
                excerpt=item.excerpt,
                source_name=PORTO_CENTRAL_SOURCE_NAME,
                published_at=item.published_at,
                updated_at=item.updated_at,
                scrapped_at=now,
                url=item.url,
                author=author,
            )
            db.session.add(article)
            created += 1
            continue

        article.title = item.title
        article.html_content = item.html_content
        article.excerpt = item.excerpt
        article.source_name = PORTO_CENTRAL_SOURCE_NAME
        article.published_at = item.published_at
        article.updated_at = item.updated_at
        article.scrapped_at = now
        article.url = item.url
        article.author = author
        updated += 1

    db.session.commit()
    return created, updated


def parse_post(post: dict) -> ScrapedArticle:
    embedded_author = post.get("_embedded", {}).get("author", [{}])[0]

    return ScrapedArticle(
        news_id=int(post["id"]),
        title=_html_to_text(post.get("title", {}).get("rendered", "")),
        html_content=post.get("content", {}).get("rendered", ""),
        excerpt=_html_to_text(post.get("excerpt", {}).get("rendered", "")),
        url=post.get("link", ""),
        published_at=_parse_wp_datetime(post.get("date")),
        updated_at=_parse_wp_datetime(post.get("modified")),
        author_name=embedded_author.get("name") or "Porto Central",
        author_about=embedded_author.get("description") or "",
    )


def _get_or_create_author(item: ScrapedArticle, now: datetime) -> Authors:
    author = Authors.query.filter_by(name=item.author_name).first()
    if author is None:
        author = Authors(
            name=item.author_name,
            about=item.author_about,
            created_at=now,
        )
        db.session.add(author)
    elif item.author_about and author.about != item.author_about:
        author.about = item.author_about

    return author


def _parse_wp_datetime(value):
    if not value:
        return datetime.utcnow()
    return datetime.fromisoformat(value)


def _html_to_text(value):
    parser = _TextExtractor()
    parser.feed(value or "")
    return unescape(parser.text())
