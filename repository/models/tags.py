from sqlalchemy.orm import Mapped, mapped_column
from repository.ext.db import db


class Tags(db.Model):
    __tablename__ = "tags"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
