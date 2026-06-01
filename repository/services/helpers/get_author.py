from datetime import datetime

from repository.ext.db import db
from repository.models import Authors
from repository.services.helpers.scrapped_article import ScrapedArticle


def get_author(item: ScrapedArticle, now: datetime) -> Authors:
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
