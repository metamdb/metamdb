# type: ignore
from sqlalchemy import func
from datetime import datetime

from src import db


class CasmUser(db.Model):
    __abstract__ = True
    __bind_key__ = 'casm_user'


class User(CasmUser):
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(3), nullable=False, unique=True)
    email: str = db.Column(db.String(100), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)
    date: datetime = db.Column(db.DateTime(timezone=True),
                               default=func.now(),
                               nullable=False)
