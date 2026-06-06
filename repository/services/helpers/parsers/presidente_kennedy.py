from datetime import datetime, UTC

from bs4 import BeautifulSoup

from repository.services.helpers.scrapped_article import ScrapedArticle

PRESIDENTE_KENNEDY_SOURCE_NAME = "Prefeitura de Presidente Kennedy"


def parse_presidente_kennedy_post(
        html_content: str,
        url: str,
) -> ScrapedArticle:
    print(f"Parsing {url}")
    soup = BeautifulSoup(html_content, "html.parser")

    title_tag = soup.select_one(".banner-top-news .title")
    title = title_tag.get_text(" ", strip=True) if title_tag else "Sem título"
    article_tag = soup.select_one(".text-news")
    article_html = str(article_tag) if article_tag else ""
    excerpt = article_tag.get_text(" ", strip=True)[:500] if article_tag else ""

    published_at = datetime.now(UTC)

    publication_tag = soup.find(
        string=lambda text: text and "Data de Publicação:" in text
    )

    if publication_tag:
        try:
            date_text = publication_tag.replace("Data de Publicação:", "").strip()

            published_at = datetime.strptime(date_text, "%d/%m/%Y às %H:%M:%S").replace(
                tzinfo=UTC
            )

        except ValueError:
            pass

    # Autor/Fonte
    source_tag = soup.find(
        string=lambda text: text and "Fonte das Informações:" in text
    )

    author_name = "Prefeitura Presidente Kennedy"

    if source_tag:
        author_name = source_tag.replace("Fonte das Informações:", "").strip()

    try:
        news_id = int(url.rstrip("/").split("/")[-1])
    except (ValueError, TypeError):
        news_id = abs(hash(url))

    return ScrapedArticle(
        news_id=news_id,
        title=title,
        html_content=article_html,
        excerpt=excerpt,
        url=url,
        published_at=published_at,
        updated_at=published_at,
        author_name=author_name,
        author_about="Portal oficial da Prefeitura de Presidente Kennedy",
        source=PRESIDENTE_KENNEDY_SOURCE_NAME,
    )
