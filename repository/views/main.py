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
from repository.models import Articles, Article_tags, Tags

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
        current_app.logger.info(f"Mensagem recebida do {form.email.data}")
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("main.index"))
    else:
        print(form.errors)

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
