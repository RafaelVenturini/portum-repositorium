from datetime import UTC, datetime
from urllib.parse import urlparse

from repository.services.helpers.save_article import html_to_text
from repository.services.helpers.scrapped_article import ScrapedArticle


def parse_wp_datetime(value):
    if not value:
        return datetime.now(UTC)
    return datetime.fromisoformat(value)


def wp_parse_post(post: dict) -> ScrapedArticle:
    embedded_author = post.get("_embedded", {}).get("author", [{}])[0]
    url = (post.get("link", ""),)
    url = url[0]

    title = html_to_text(post.get("title", {}).get("rendered", ""))

    print(f"Collected {title} from {url}")

    return ScrapedArticle(
        news_id=int(post["id"]),
        title=title,
        html_content=post.get("content", {}).get("rendered", ""),
        excerpt=html_to_text(post.get("excerpt", {}).get("rendered", "")),
        url=url,
        published_at=parse_wp_datetime(post.get("date")),
        updated_at=parse_wp_datetime(post.get("modified")),
        author_name=embedded_author.get("name") or "Porto Central",
        author_about=embedded_author.get("description") or "",
        source=urlparse(url).netloc,
    )
