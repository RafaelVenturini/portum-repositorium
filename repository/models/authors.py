from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from repository.ext.db import db


class Authors(db.Model):
    __tablename__ = "authors"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    deleted_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    about: Mapped[str] = mapped_column(db.Text, nullable=True)

    articles = relationship("Articles", back_populates="author")
