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
    articles = Articles.query.order_by(Articles.published_at.desc()).all()
    return render_template("main/news.html", articles=articles)


@bp_main.route("/news/<int:article_id>")
def news_detail(article_id):
    article = db.session.get(Articles, article_id)
    if article is None:
        abort(404)
    return render_template("main/news_detail.html", article=article)


# @bp_main.route('/carrinho')
# def carrinho():
#     carrinho = {
#         'itens': [
#             {'id': 1, 'name': "Pizza Margherita", 'preco': 49.95, 'quantidade': 1},
#             {'id': 2, 'name': "Refrigerante 2L", 'preco': 8.52, 'quantidade': 2},
#             {'id': 3, 'name': "Borda Recheada", 'preco': 12.358, 'quantidade': 1}
#         ]
#         #'itens': []
#     }
#     total = sum(item['preco']*item['quantidade'] for item  in carrinho['itens'])
#     return render_template('main/carrinho.html',
#                            carrinho=carrinho,
#                            total=total,
#                            titulo="Meu pedido prefido")


# @bp_main.route('/contato', methods=['GET', 'POST'])
# def contato():
#     form = ContatoForm()

#     if form.validate_on_submit():
#         current_app.logger.info(f"Mensagem recebida do {form.nome.data}")
#         flash('Mensagem enviada com sucesso!', 'success')
#         return redirect(url_for('main.index'))
#     else:
#         print(form.errors)

#     return render_template('main/contato.html', form=form)
