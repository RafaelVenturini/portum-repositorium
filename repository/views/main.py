from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    flash,
    redirect,
    url_for,
)
from sqlalchemy.orm import joinedload

from repository.ext.db import db
from repository.forms.main import NewsLetterForm
from repository.models import Articles, Article_tags, Tags, Newsletter
from datetime import datetime, UTC

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
    articles = (
        Articles.query.options(
            joinedload(Articles.article_tags).joinedload(Article_tags.tag)
        )
        .order_by(Articles.published_at.desc())
        .all()
    )

    return render_template("main/news.html", articles=articles)


@bp_main.route("/news/<int:article_id>")
def news_detail(article_id):
    current_app.logger.debug("Renderizando template news_detail.html")
    article = db.session.get(Articles, article_id)
    if article is None:
        abort(404)
    return render_template("main/news_detail.html", article=article)


@bp_main.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    form = NewsLetterForm()
    current_app.logger.debug("Renderizando template newsletter.html")

    if form.validate_on_submit():
        email = form.email.data
        current_app.logger.info(f"Tentando inscrever {email} na newsletter")

        try:
            # Verifica se já existe
            existing = Newsletter.query.filter_by(email=email).first()
            if existing:
                flash("E-mail já inscrito na newsletter.", "info")
                return redirect(url_for("main.index"))

            # Cria novo registro
            n = Newsletter(
                email=email,
                subscribed_at=datetime.now(UTC),
                is_active=True,
            )
            db.session.add(n)
            db.session.commit()

            current_app.logger.info(f"E-mail {email} inscrito com sucesso")
            flash("Inscrição realizada com sucesso!", "success")
            return redirect(url_for("main.index"))

        except Exception as e:
            current_app.logger.error(f"Erro ao persistir newsletter: {e}")
            db.session.rollback()
            flash("Ocorreu um erro ao processar sua inscrição.", "danger")

    else:
        if form.errors:
            current_app.logger.debug(f"Erros no formulário: {form.errors}")

    return render_template("main/newsletter.html", form=form)


@bp_main.route("/tags/<int:tag_id>")
def tags(tag_id):
    current_app.logger.debug(f"Renderiznado news.html com apenas a tag {tag_id}")
    articles = (
        Articles.query.join(Articles.article_tags)
        .filter(Article_tags.tag_id == tag_id)
        .order_by(Articles.published_at.desc())
        .all()
    )
    tag = Tags.query.get(tag_id)

    return render_template("main/news.html", articles=articles, tag=tag)


@bp_main.route("/about")
def about():
    return render_template("main/about.html")
