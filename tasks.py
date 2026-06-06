import os
import zipfile
from datetime import datetime

from dotenv import load_dotenv
from invoke import task


# ==========================================================
# GERENCIAMENTO DE AMBIENTE
# ==========================================================
def load_env(env: str):
    """
    Carrega o arquivo .env correspondente ao ambiente.
    Ex: dev, test, prod
    """
    env_file = f".env.{env}"

    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
        print(f"[ENV] Carregado: {env_file}")
    else:
        raise FileNotFoundError(f"{env_file} nao encontrado")


# ==========================================================
# INSTALACAO
# ==========================================================
@task
def install(c, dev=True):
    """
    Instala o projeto.
    """
    if dev:
        c.run('pip install -e ".[dev,test]"', echo=True)
    else:
        c.run("pip install .", echo=True)


@task
def uninstall(c):
    """
    Remove o pacote instalado.
    """
    c.run("pip uninstall -y repository", echo=True)


# ==========================================================
# EXECUCAO
# ==========================================================
@task
def run(c):
    """
    Executa a aplicacao Flask em ambiente de desenvolvimento.
    """
    load_env("dev")
    c.run("flask run")


@task
def prod(c):
    """
    Executa a aplicacao em modo producao.
    """
    load_env("prod")
    c.run("flask run")


# ==========================================================
# TESTES
# ==========================================================
@task
def test(c):
    """
    Executa os testes automatizados.
    """
    load_env("test")
    c.run("PYTHONPATH=. pytest -v")


# ==========================================================
# QUALIDADE DE CODIGO
# ==========================================================
@task
def lint(c):
    """
    Verifica qualidade de codigo.
    """
    c.run("flake8")


@task
def format(c):
    """
    Formata o codigo automaticamente.
    """
    c.run("black .")


# ==========================================================
# EMPACOTAMENTO
# ==========================================================
@task
def zip(c, name=None):
    """
    Cria um arquivo ZIP do projeto para entrega, excluindo cache e arquivos sensíveis.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_filename = name or f"portum-repositorium-{timestamp}.zip"

    # diretório do projeto a ser empacotado (raiz do repositório)
    project_root = os.path.abspath('.')

    # colocamos o ZIP de saída dentro de `uvv/` por compatibilidade com o repositório,
    # mas NÃO iremos percorrer esse diretório ao gerar o ZIP (evita incluir zips anteriores)
    output_dir = os.path.abspath(os.path.join("uvv"))
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, zip_filename)

    print(f"→ Criando ZIP: {zip_path}")

    # pastas e padrões de arquivo a excluir
    excludes = [
        "venv", ".venv", "__pycache__", ".git", ".vscode", ".pytest_cache",
        "dist", "build", "*.egg-info", "node_modules", "instance"
    ]

    exclude_extensions = (".pyc", ".pyo", ".pyd", ".log", ".db", ".sqlite3", ".lock")
    exclude_patterns = [".env", ".env."]  # arquivos .env e .env.* (sensíveis)

    # Gera o ZIP caminhando pela raiz do projeto, mas excluindo pastas listadas em `excludes`.
    # Também garantimos que o diretório de saída (`uvv`) NÃO será percorrido para evitar incluir
    # arquivos grandes já existentes (ex.: zips anteriores).
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Nome das pastas no nível atual
            # Evita traversal em diretórios excluídos
            dirs[:] = [d for d in dirs if d not in excludes and os.path.abspath(os.path.join(root, d)) != output_dir]

            for file in files:
                # pula arquivos com extensões excluídas
                if file.endswith(exclude_extensions):
                    continue

                # pula arquivos sensíveis (.env, .env.*)
                if file == ".env" or file.startswith(".env."):
                    continue

                filepath = os.path.join(root, file)

                # evita adicionar o próprio arquivo ZIP de saída ao arquivo (pode causar crescimento indefinido)
                try:
                    if os.path.abspath(filepath) == os.path.abspath(zip_path):
                        continue
                except Exception:
                    pass

                # adiciona ao zip mantendo estrutura relativa à raiz do projeto
                arcname = os.path.relpath(filepath, project_root)
                zipf.write(filepath, arcname=arcname)

    if os.path.exists(zip_path):
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"✓ ZIP criado com sucesso!")
        print(f"  Caminho: {zip_path}")
        print(f"  Tamanho: {size_mb:.2f} MB")
    else:
        print(f"✗ Erro ao criar ZIP")
