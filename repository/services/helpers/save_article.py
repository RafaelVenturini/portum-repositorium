from datetime import datetime, UTC
from typing import Iterable

from bs4 import BeautifulSoup

from repository.ext.db import db
from repository.models import Articles, Article_tags, Tags
from repository.services.helpers.get_author import get_author
from repository.services.helpers.parsers.html_parser import sanitize_html
from repository.services.helpers.scrapped_article import ScrapedArticle
from repository.services.helpers.tagger import tag_news


def html_to_text(value):
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(separator=" ", strip=True)


def save_articles(articles: Iterable[ScrapedArticle]) -> tuple[int, int]:
    created = 0
    updated = 0
    now = datetime.now(UTC)

    for item in articles:
        author = get_author(item, now)
        article = Articles.query.filter_by(news_id=item.news_id).first()
        tags = tag_news(item.title, item.html_content)

        if article is None:
            article = Articles(
                news_id=item.news_id,
                title=item.title,
                html_content=sanitize_html(item.html_content),
                excerpt=item.excerpt,
                published_at=item.published_at,
                updated_at=item.updated_at,
                scrapped_at=now,
                url=item.url,
                author_id=author.id,
            )

            db.session.add(article)
            for tag in tags:
                tag_id = Tags.query.filter_by(name=tag).first().id
                article_tags = Article_tags(article_id=article.id, tag_id=tag_id)
                db.session.add(article_tags)
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

        for tag in tags:
            tag_id = Tags.query.filter_by(name=tag).first().id
            tag_exists = Article_tags.query.filter_by(
                article_id=article.id, tag_id=tag_id
            ).first()
            if tag_exists:
                continue
            article_tags = Article_tags(article_id=article.id, tag_id=tag_id)
            db.session.add(article_tags)

        updated += 1

    db.session.commit()
    return created, updated
