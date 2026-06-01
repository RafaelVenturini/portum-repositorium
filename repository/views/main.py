from flask import Blueprint, abort, current_app, render_template

from repository.ext.db import db
from repository.models import Articles

# from repository.forms.main import NewsLetterForm

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
@bp_main.route("/index")
def index():
    current_app.logger.debug("Renderizando template index.html")
    articles = Articles.query.order_by(Articles.published_at.desc()).limit(5).all()
    return render_template("main/index.html", articles=articles)


@bp_main.route("/news")
def news():
    current_app.logger.debug("Renderizando template news.html")
    articles = Articles.query.order_by(Articles.published_at.desc()).all()
    return render_template("main/news.html", articles=articles)


@bp_main.route("/news/<int:article_id>")
def news_detail(article_id):
    current_app.logger.debug("Renderizando template news_detail.html")
    article = db.session.get(Articles, article_id)
    if article is None:
        abort(404)
    return render_template("main/news_detail.html", article=article)


@bp_main.route("/newsletter")
def newsletter():
    current_app.logger.debug("Renderizando template newsletter.html")
    return render_template("main/newsletter.html")
