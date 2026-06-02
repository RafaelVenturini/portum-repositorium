import click

from repository.ext.db import db
from repository.ext.db.seed import seed_db


def init_app(app):
    @app.cli.command("create-db")
    def create_db():
        """Cria as tabelas do db."""

        db.create_all()
        click.echo("Banco de dados criado com sucesso!")

    @app.cli.command("drop-db")
    def drop_db():
        """Remove todas as tabelas do db."""

        db.drop_all()
        click.echo("Banco de dados removido com sucesso!")

    @app.cli.command("scrape-news")
    @click.option(
        "--limit", default=5, show_default=True, help="Quantidade de noticias."
    )
    @click.option("--page", default=1, show_default=True, help="Pagina da API.")
    @click.option(
        "--order",
        default="desc",
        show_default=True,
        type=click.Choice(["asc", "desc"]),
        help="Ordenacao por data de publicacao.",
    )
    def scrape_news(limit, page, order):
        """Busca noticias do Porto Central e salva no SQLite."""
        from repository.services.scrappers.porto_central import (
            save_articles,
            scrape_porto_central,
        )

        db.create_all()
        articles = scrape_porto_central(limit=limit, page=page, order=order)
        created, updated = save_articles(articles)
        click.echo(f"Scraping finalizado: {created} criadas, {updated} atualizadas.")

    @app.cli.command("seed-db")
    def seed_db_cli():
        """Popula o banco de dados."""
        seed_db()

        print("Seed executado com sucesso.")

    @app.cli.command("reset-database")
    def reset_database():
        """Reconstroi todo o banco de dados para debug"""

        db.drop_all()
        db.create_all()
        seed_db()
        print("Banco recriado com sucesso!")
