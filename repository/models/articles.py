from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from repository.ext.db import db


class Articles(db.Model):
    __tablename__ = "articles"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    news_id: Mapped[int] = mapped_column(
        db.Integer, nullable=False, unique=True, index=True
    )
    title: Mapped[str] = mapped_column(db.String(255), nullable=False, index=True)
    html_content: Mapped[str] = mapped_column(db.Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(db.Text, nullable=True)
    source_name: Mapped[str] = mapped_column(
        db.String(120), nullable=False, default="Porto Central"
    )
    published_at: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    scrapped_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    url: Mapped[str] = mapped_column(
        db.String(255), nullable=False, unique=True, index=True
    )
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("authors.id"), nullable=True
    )
    previous_version_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("articles.id"), nullable=True
    )

    author = relationship("Authors", back_populates="articles")
