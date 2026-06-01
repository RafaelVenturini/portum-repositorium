from datetime import datetime, UTC
from html import unescape
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urlparse

from repository.ext.db import db
from repository.models import Articles
from repository.services.helpers.get_author import get_author
from repository.services.helpers.scrapped_article import ScrapedArticle


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.parts.append(value)

    def text(self):
        return " ".join(self.parts)


def save_articles(articles: Iterable[ScrapedArticle]) -> tuple[int, int]:
    created = 0
    updated = 0
    now = datetime.now(UTC)

    for item in articles:
        author = get_author(item, now)
        article = Articles.query.filter_by(news_id=item.news_id).first()

        if article is None:
            article = Articles(
                news_id=item.news_id,
                title=item.title,
                html_content=item.html_content,
                excerpt=item.excerpt,
                published_at=item.published_at,
                updated_at=item.updated_at,
                scrapped_at=now,
                url=item.url,
                author_id=author.id,
            )
            db.session.add(article)
            created += 1
            continue

        article.title = item.title
        article.html_content = item.html_content
        article.excerpt = item.excerpt
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
    url = (post.get("link", ""),)
    url = url[0]

    return ScrapedArticle(
        news_id=int(post["id"]),
        title=html_to_text(post.get("title", {}).get("rendered", "")),
        html_content=post.get("content", {}).get("rendered", ""),
        excerpt=html_to_text(post.get("excerpt", {}).get("rendered", "")),
        url=url,
        published_at=parse_wp_datetime(post.get("date")),
        updated_at=parse_wp_datetime(post.get("modified")),
        author_name=embedded_author.get("name") or "Porto Central",
        author_about=embedded_author.get("description") or "",
        source=urlparse(url).netloc,
    )


def parse_wp_datetime(value):
    if not value:
        return datetime.now(UTC)
    return datetime.fromisoformat(value)


def html_to_text(value):
    parser = TextExtractor()
    parser.feed(value or "")
    return unescape(parser.text())
