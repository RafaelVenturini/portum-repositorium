from repository.ext.db import db
from repository.ext.db.tags import tags_list
from repository.models import Tags
import logging

# scrapers and saver
from repository.services.scrappers.porto_central import scrape_porto_central
from repository.services.scrappers.presidente_kennedy import scrape_presidente_kennedy
from repository.services.helpers.save_article import save_articles

logger = logging.getLogger(__name__)


def seed_db():
    """Cria todas os dados cruciais para o banco.

    Atualmente faz:
    - create_all (garante que tabelas existam)
    - insere tags iniciais
    - realiza scraping básico e salva noticias
    """

    # garante tabelas existam
    db.create_all()

    for tag in tags_list:
        if not Tags.query.filter_by(name=tag["name"]).first():
            db.session.add(Tags(name=tag["name"]))

    db.session.commit()

    # Opcional: realiza um scraping leve para popular noticias iniciais
    try:
        logger.info("Executando seed: scraping inicial do Porto Central")
        port_articles = scrape_porto_central(limit=5, page=1, order="desc")
        created, updated = save_articles(port_articles)
        logger.info("Porto Central: %d criadas, %d atualizadas durante seed", created, updated)

        logger.info("Executando seed: scraping inicial do site da prefeitura")
        gov_articles = scrape_presidente_kennedy()
        g_created, g_updated = save_articles(gov_articles)
        logger.info("Prefeitura: %d criadas, %d atualizadas durante seed", g_created, g_updated)

    except Exception as e:
        logger.exception("Erro durante seed com scraping: %s", e)

