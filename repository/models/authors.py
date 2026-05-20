from sqlalchemy.orm import Mapped, mapped_column
from repository.ext.db import db


class Authors(db.Model):
    __tablename__ = "authors"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = (mapped_column(db.String(255), nullable=False, unique=True),)
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)
    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False)
    about: Mapped[str] = mapped_column(db.Text, nullable=True)
