import click
import random
from delivery.ext.db import db
from delivery.models import (
    User, Role, RoleUser, Level, Business, BusinessType, City, Address
)

def init_app(app):

    @app.cli.command("create-db")
    def create_db():
        """Cria todas as tabelas do banco de dados."""
        # Garantimos que os modelos foram carregados via __init__
        import delivery.models 
        db.create_all()
        click.echo("Banco de dados materializado com sucesso!")

    @app.cli.command("seed-base")
    def seed_base():
        """Popula tabelas de domínio (Níveis, Papéis e Tipos de Negócio)."""
        try:
            # 1. Níveis
            levels = [
                ("God", "Acesso total ao sistema"),
                ("Premium", "Nível gerencial superior"),
                ("Basic", "Nível operacional"),
                ("Standard", "Nível padrão de cliente")
            ]
            for name, desc in levels:
                if not Level.query.filter_by(name=name).first():
                    db.session.add(Level(name=name, description=desc))

            # 2. Papéis
            roles = ["Administrador", "Gerente", "Operador", "Cliente"]
            for name in roles:
                if not Role.query.filter_by(name=name).first():
                    db.session.add(Role(name=name))

            # 3. Tipos de Negócio
            b_types = ["Pizzaria", "Hamburgueria", "Restaurante", "Farmácia"]
            for name in b_types:
                if not BusinessType.query.filter_by(name=name).first():
                    db.session.add(BusinessType(name=name))

            db.session.commit()
            click.echo("Dados de domínio (Levels, Roles, BusinessTypes) inseridos.")
        except Exception as e:
            db.session.rollback()
            click.echo(f"Erro no seed-base: {e}")

    @app.cli.command("seed-test-data")
    def seed_test_data():
        """Cria um cenário de teste completo: Usuário, Empresa e Vínculo."""
        try:
            # Recupera bases
            level_god = Level.query.filter_by(name="God").first()
            role_admin = Role.query.filter_by(name="Administrador").first()
            type_pizza = BusinessType.query.filter_by(name="Pizzaria").first()

            if not all([level_god, role_admin, type_pizza]):
                click.echo("Erro: Execute 'flask seed-base' primeiro.")
                return

            # Criar Usuário João
            joao = User.query.filter_by(email="joao@delivery.com").first()
            if not joao:
                joao = User(
                    name="João Silva",
                    email="joao@delivery.com",
                    cpf="111.111.111-11"
                )
                db.session.add(joao)
                db.session.flush()

            # Criar Empresa
            if not Business.query.filter_by(cnpj="12.345/0001-99").first():
                pizza = Business(
                    owner=joao,
                    corporate_name="Pizzaria João LTDA",
                    trade_name="Suprema Pizza",
                    cnpj="12.345/0001-99",
                    business_type=type_pizza
                )
                db.session.add(pizza)
                db.session.flush()

                # Criar Vínculo de acesso (RoleUser)
                vinculo = RoleUser(
                    user=joao,
                    role=role_admin,
                    business=pizza,
                    level=level_god
                )
                db.session.add(vinculo)

            db.session.commit()
            click.echo("Cenário de teste (João + Suprema Pizza) criado com sucesso!")
        except Exception as e:
            db.session.rollback()
            click.echo(f"Erro no seed-test-data: {e}")

    @app.cli.command("drop-db")
    @click.confirmation_option(prompt="Tem certeza que deseja apagar TUDO?")
    def drop_db():
        """Remove todas as tabelas do banco (Cuidado!)."""
        db.drop_all()
        click.echo("Banco de dados removido.")