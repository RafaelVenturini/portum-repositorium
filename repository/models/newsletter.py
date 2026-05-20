from sqlalchemy.orm import Mapped, mapped_column, relationship
from repository.ext.db import db

class Newsletter(db.Model):
    __tablename__ = "newsletter"
    __table_args__ = {'extend_existing': True}
    
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True, index=True)
    subscribed_at: Mapped[str] = mapped_column(db.DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)
    cancelled_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)
    