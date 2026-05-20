from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    redirect,
    url_for,
    request,
)
from delivery.forms.main import ContatoForm

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
@bp_main.route("/index")
def index():
    current_app.logger.debug("Renderizando template index.html")
    user = {"username": "wanderson"}
    return render_template(
        "main/index.html",
        user=user,
        promocao="Segunda é dia de Pizza em dobro!!!",
    )


@bp_main.route("/carrinho")
def carrinho():
    carrinho = {
        "itens": [
            {
                "id": 1,
                "name": "Pizza Margherita",
                "preco": 49.95,
                "quantidade": 1,
            },
            {
                "id": 2,
                "name": "Refrigerante 2L",
                "preco": 8.52,
                "quantidade": 2,
            },
            {
                "id": 3,
                "name": "Borda Recheada",
                "preco": 12.358,
                "quantidade": 1,
            },
        ]
        #'itens': []
    }
    total = sum(item["preco"] * item["quantidade"] for item in carrinho["itens"])
    return render_template(
        "main/carrinho.html",
        carrinho=carrinho,
        total=total,
        titulo="Meu pedido prefido",
    )


@bp_main.route("/contato", methods=["GET", "POST"])
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        current_app.logger.info(f"Mensagem recebida do {form.nome.data}")
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("main.index"))
    else:
        print(form.errors)

    return render_template("main/contato.html", form=form)
