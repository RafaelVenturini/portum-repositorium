import logging
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    # Configuracao recomendada para desenvolvimento:
    # Mostra mensagens DEBUG e INFO no console
    if app.debug:
        app.logger.setLevel(logging.DEBUG)

    # ----------------------------------------------------------
    # Configuracao da aplicacao (variaveis de ambiente)
    # ----------------------------------------------------------
    from repository.ext.config import init_app as init_config

    init_config(app)

    if test_config:
        app.config.update(test_config)

    # ----------------------------------------------------------
    # Inicializacao do banco de dados
    # ----------------------------------------------------------
    from repository.ext.db import init_app as init_db

    init_db(app)

    # Registro dos modelos no metadata do SQLAlchemy
    from repository.ext.db import register_models

    register_models()

    # ----------------------------------------------------------
    # Outras extensoes
    # ----------------------------------------------------------
    if not app.config.get("TESTING"):
        from repository.ext.wtf import init_app as init_wtf

        init_wtf(app)

    from repository.ext.debugtoolbar import init_app as init_toolbar

    init_toolbar(app)

    from repository.ext.cli import init_app as init_cli

    init_cli(app)

    # ----------------------------------------------------------
    # Blueprints (camada de apresentacao)
    # ----------------------------------------------------------
    from repository.views import init_app as init_site

    init_site(app)

    return app
