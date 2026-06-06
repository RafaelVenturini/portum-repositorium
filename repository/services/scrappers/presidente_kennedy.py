from urllib.request import urlopen, Request
import logging

from bs4 import BeautifulSoup

from repository.services.helpers.parsers.presidente_kennedy import (
    parse_presidente_kennedy_post,
)
from repository.services.helpers.request_headers import headers
from repository.services.helpers.scrapped_article import ScrapedArticle

logger = logging.getLogger(__name__)


def fetch_presidente_kennedy_posts():
    url = "https://presidentekennedy.es.gov.br/noticias?content_terms=Porto+Central"

    request = Request(url, headers=headers)

    try:
        with urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")

    except Exception as e:
        logger.error("Erro ao buscar lista de noticias da Prefeitura: %s", e)
        return []

    soup = BeautifulSoup(html, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a.get("href")

        if (
            isinstance(href, str)
            and href.startswith("https://presidentekennedy.es.gov.br/noticia/")
            and href not in links
        ):
            logger.debug("Encontrada referencia de noticia: %s", href)
            links.append(href)

    return links


def fetch_presidente_kennedy_post(news_urls: list[str]) -> list[ScrapedArticle]:
    articles = []

    for url in news_urls:
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
                    )
                },
            )


            with urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8")

            logger.debug("Processando notícia: %s", url)

            articles.append(
                parse_presidente_kennedy_post(
                    html_content=html,
                    url=url,
                )
            )

        except Exception as e:
            logger.error("Erro ao processar %s: %s", url, e)

    return articles


def scrape_presidente_kennedy():
    news_urls = fetch_presidente_kennedy_posts()
    return fetch_presidente_kennedy_post(news_urls)
