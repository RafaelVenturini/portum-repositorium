from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def register_models():
    """
    Importa todos os modulos que definem modelos para que sejam registrados
    no metadata do SQLAlchemy antes de operacoes como create_all().
    """
    import repository.models.article_tags
    import repository.models.articles
    import repository.models.authors
    import repository.models.tags
    import repository.models.newsletter
