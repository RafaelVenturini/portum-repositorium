from datetime import datetime, UTC
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from repository.services.helpers.scrapped_article import ScrapedArticle

PRESIDENTE_KENNEDY_URL = (
    "https://presidentekennedy.es.gov.br/noticias?content_terms=Porto+Central"
)
PRESIDENTE_KENNEDY_SOURCE_NAME = "Prefeitura de Presidente Kennedy"


def fetch_presidente_kennedy_posts(html_snippet: str, base_url: str) -> ScrapedArticle:
    """
    Recebe um pedaço de HTML representando UMA notícia e devolve um ScrapedArticle.
    """
    soup = BeautifulSoup(html_snippet, "html.parser")
    html_title = (soup.find("p", class_="title"),)
    html_article = (soup.find("div", class_="text-news"),)

    title = html_title.get_text(strip=True) if html_title else "Sem Título"
    raw_url = html_title["href"] if html_title and html_title.has_attr("href") else ""
    full_url = urljoin(base_url, raw_url)
    excerpt = html_article.get_text(strip=True) if html_article else ""
    # Tratando a Data (Aqui você chama uma função sua para converter "12/05/2026" pra datetime)
    date_str = date_tag.get_text(strip=True) if date_tag else ""
    try:
        # Exemplo: se o formato for DD/MM/YYYY
        # published_at = datetime.strptime(date_str, "%d/%m/%Y")
        # Se você já tiver um helper de data para isso, chame-o aqui!
        published_at = datetime.now(UTC)  # Fallback seguro
    except ValueError:
        published_at = datetime.now(UTC)

    # 4. CRIAÇÃO DO ID ÚNICO
    # Sites sem API não tem um "ID" explícito.
    # Uma tática comum é extrair o ID da URL (ex: /noticia/3445 -> 3445)
    # ou usar a URL inteira (hasheada ou não) como chave.

    # Exemplo: pegando o último trecho da URL separada por "/"
    try:
        # Se a url for prefeitura.es.gov.br/noticia/3445, isso pega "3445"
        news_id_str = full_url.rstrip("/").split("/")[-1]
        news_id = int(news_id_str)
    except ValueError:
        # Se não conseguir um int da URL, gera um hash seguro pra garantir unicidade
        news_id = hash(full_url)
    return ScrapedArticle(
        news_id=news_id,
        title=title,
        html_content=str(soup),
        excerpt=excerpt,
        url=full_url,
        published_at=published_at,
        updated_at=published_at,
        author_name="Prefeitura Presidente Kennedy",
        author_about="Mural de notícias da gestão municipal",
        source=urlparse(base_url).netloc,
    )
