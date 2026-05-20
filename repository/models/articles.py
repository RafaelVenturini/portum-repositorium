from sqlalchemy.orm import Mapped, mapped_column, relationship
from repository.ext.db import db

class Articles(db.Model):
    __tablename__ = "articles"
    __table_args__ = {'extend_existing': True}
    
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    html_content: Mapped[str] = mapped_column(db.Text, nullable=False)
    scrapped_at: Mapped[str] = mapped_column(db.DateTime, nullable=False)
    url: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(db.String(255), nullable=True)
    previous_version_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('articles.id'), nullable=True)
    