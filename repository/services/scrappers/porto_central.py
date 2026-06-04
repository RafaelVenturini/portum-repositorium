import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..helpers.scrapped_article import ScrapedArticle
from ..helpers.word_press import wp_parse_post

PORTO_CENTRAL_POSTS_URL = "https://www.portocentral.com.br/wp-json/wp/v2/posts"
PORTO_CENTRAL_SOURCE_NAME = "Porto Central"


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
        return json.load(response), url


def scrape_porto_central(limit=5, page=1, order="desc") -> list[ScrapedArticle]:
    posts, url = fetch_porto_central_posts(limit=limit, page=page, order=order)
    return [wp_parse_post(post) for post in posts]
