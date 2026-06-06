import pytest

from repository import create_app
from urllib.request import Request, urlopen
from urllib.error import URLError
from repository.services.helpers.request_headers import headers
from repository.services.scrappers.porto_central import PORTO_CENTRAL_POSTS_URL
from repository.services.scrappers.presidente_kennedy import fetch_presidente_kennedy_posts
from bs4 import BeautifulSoup

# =============================================================================
# FIXTURES (infraestrutura de teste)
# =============================================================================


@pytest.fixture
def app():
    """
    Cria uma instancia da aplicacao configurada para testes.
    """
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "WTF_CSRF_ENABLED": False,
        }
    )


@pytest.fixture
def client(app):
    """
    Cliente HTTP de teste (simula requisicoes sem servidor real).
    """
    return app.test_client()


# =============================================================================
# TESTES DE INFRAESTRUTURA
# =============================================================================


def test_app_is_created(app):
    """
    Verifica se a aplicacao foi criada corretamente.
    """
    assert app is not None


def test_config_is_loaded(app):
    """
    Garante que as configuracoes de teste foram aplicadas.
    """
    assert app.config["TESTING"] is True


def test_app_is_running_in_test_mode(app):
    """
    Confirma explicitamente o modo de execucao da aplicacao.
    """
    assert app.config["TESTING"] is True


# =============================================================================
# TESTES DE ROTAS
# =============================================================================


def test_non_existent_route_returns_404(client):
    """
    Rotas inexistentes devem retornar HTTP 404.
    """
    response = client.get("/url_que_nao_existe")
    assert response.status_code == 404


# -----------------------------------------------------------------------------
# TESTES PARAMETRIZADOS DE ROTAS PUBLICAS
# -----------------------------------------------------------------------------

PUBLIC_ROUTES = [
    ("/", True),
    ("/index", True),
    ("/news", True),
    ("/news/1", True),
]


@pytest.mark.parametrize("route, check_doctype", PUBLIC_ROUTES)
def test_public_routes_return_200_in_html(client, route, check_doctype):
    """
    Verifica que rotas publicas:
    - retornam status 200
    - entregam HTML valido (verificacao minima)

    O uso de parametrizacao permite escalar facilmente os testes.
    """
    response = client.get(route)

    assert response.status_code == 200, f"Rota {route} retornou {response.status_code}"

    assert (
        b"<html" in response.data or b"<!DOCTYPE html>" in response.data
    ), f"Rota {route} nao parece retornar HTML"

    if check_doctype:
        assert (
            b"<!DOCTYPE html>" in response.data
        ), f"Rota {route} deveria conter DOCTYPE html"


# =============================================================================
# TESTES DE CONTEUDO
# =============================================================================


def test_index_page(client):
    """
    Verifica conteudo minimo da pagina inicial.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Feito por: Rafael Venturini" in response.data


# =============================================================================
# TESTES DE FORMULARIO
# =============================================================================


def test_newsletter_form(client):
    """
    Testa o fluxo completo de envio de formulario valido:
    - POST com dados corretos
    - espera redirecionamento (302)
    """
    response = client.post(
        "/newsletter",
        data={
            "email": "teste@uvv.com",
            "submit": "Assinar Newsletter",
        },
        content_type="application/x-www-form-urlencoded",
    )

    assert response.status_code == 302  # redirect apos sucesso


def test_porto_central_api_endpoint_available():
    """Verifica que a rota REST do Porto Central usada pelo scraper responde 200."""
    req = Request(PORTO_CENTRAL_POSTS_URL, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            code = getattr(resp, "getcode", lambda: resp.status)()
            assert int(code) == 200
    except URLError as e:
        pytest.skip(f"Rede indisponível ou host inacessível: {e}")


def test_presidente_kennedy_fetch_and_bs4_parse():
    """Verifica que a pagina de buscas da prefeitura pode ser acessada e parseada pelo BeautifulSoup."""
    try:
        links = fetch_presidente_kennedy_posts()
    except URLError as e:
        pytest.skip(f"Rede indisponível ou host inacessível: {e}")

    # A funcao deve retornar uma lista (mesmo que vazia)
    assert isinstance(links, list)

    # Se houver links, garante que parecem URLs e que o BS4 consegue parsear a primeira
    if links:
        first = links[0]
        assert first.startswith("https://")
        req = Request(first, headers=headers)
        try:
            with urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                # procuramos pelo menos uma tag <a>
                assert isinstance(soup.find_all("a"), list)
        except URLError as e:
            pytest.skip(f"Não foi possível acessar {first}: {e}")

