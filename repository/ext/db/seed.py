from repository.ext.db import db
from repository.ext.db.tags import tags_list
from repository.models import Tags


def seed_db():
    """Cria todas os dados cruciais para o banco. Atualmente: Tags"""

    for tag in tags_list:
        if not Tags.query.filter_by(name=tag["name"]).first():
            db.session.add(Tags(name=tag["name"]))

    db.session.commit()
