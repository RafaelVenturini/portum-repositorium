from bs4 import BeautifulSoup


def sanitize_html(html: str) -> str:
    """Limpa o html das noticias, deixando apenas as tags de html referentes a textos, e removendo tudo que não importa mais (classe, id, script, style...)"""
    soup = BeautifulSoup(html, "html.parser")

    allowed_tags = {
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "blockquote",
        "strong",
        "b",
        "em",
        "i",
        "a",
        "br",
    }

    for tag in soup.find_all(
            [
                "img",
                "svg",
                "script",
                "style",
                "iframe",
                "noscript",
                "video",
                "audio",
                "picture",
                "source",
            ]
    ):
        tag.decompose()

    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
            continue

        if tag.name == "a":
            href = tag.get("href")
            tag.attrs = {}

            if href:
                tag["href"] = href
        else:
            tag.attrs = {}

    return str(soup)
