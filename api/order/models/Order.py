from typing import List
from datetime import datetime
from db import db


def OrderCode(context):
    import random
    import string
    import time
    val = time.strftime("%S%M")
    letters = string.ascii_letters
    joined = 'ORD' + val + ''.join(random.choice(letters) for i in range(4))
    return joined


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(96), unique=True, default=OrderCode)
    customer_name = db.Column(db.String(100), nullable=False, unique=True)
    # date_deliver = db.Column(db.String(100), nullable=False, unique=True)
    cost = db.Column(db.Float(), nullable=True, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_code(cls, code: str) -> "OrderModel":
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
