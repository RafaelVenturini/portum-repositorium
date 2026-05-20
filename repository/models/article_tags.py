from sqlalchemy.orm import Mapped, mapped_column, relationship
from repository.ext.db import db

class Article_Tags(db.Model):
    __tablename__ = "article_tags"
    __table_args__ = {'extend_existing': True}

    article_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    tag_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    article = relationship("Articles", backref="article_tags")
    tag = relationship("Tags", backref="article_tags")    