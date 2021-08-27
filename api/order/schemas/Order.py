from ma import ma
from api.order.models.Order import OrderModel
from marshmallow import fields, validates, ValidationError


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        dump_only = ("id",)
        include_fk = True


class OrderSchemaSave(ma.Schema):
    class Meta:
        fields = ("customer_name", "cost",)
