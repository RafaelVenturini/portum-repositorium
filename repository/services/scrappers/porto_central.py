import json
import logging
from socket import timeout
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from repository.services.helpers.parsers.word_press import wp_parse_post
from ..helpers.request_headers import headers
from ..helpers.scrapped_article import ScrapedArticle

logger = logging.getLogger(__name__)

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
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response), url

    except timeout:
        logger.error("Timeout ao acessar Porto Central")
        return [], url

    except URLError as e:
        logger.error(f"Erro de rede ao acessar Porto Central: {e}")
        return [], url

    except Exception as e:
        logger.exception("Erro inesperado ao buscar posts do Porto Central")
        return [], url


def scrape_porto_central(limit=5, page=1, order="desc") -> list[ScrapedArticle]:
    posts, url = fetch_porto_central_posts(limit=limit, page=page, order=order)
    return [wp_parse_post(post) for post in posts]
