from flask_restful import Resource
from flask import request
from api.order.models.Order import OrderModel
from api.order.schemas.Order import OrderSchema

from marshmallow import ValidationError

order_schema = OrderSchema()
order_list_schema = OrderSchema(many=True)


class Order(Resource):
    @classmethod
    def get(cls, name: str):
        store = OrderModel.find_by_name(name)
        if store:
            return order_schema.dump(store), 200

        return {"message": "store_not_found"}, 404

    @classmethod
    def put(cls, code: str):
        from api.order.schemas.Order import OrderSchemaSave
        body = request.get_json()
        schema = OrderSchemaSave()

        try:
            schema.load(body)
            instance = OrderModel.find_by_code(code)
            instance.customer_name = request.json['customer_name']
            instance.cost = request.json['cost']
            instance.save_to_db()
            return order_schema.dump(instance), 201
        except Exception as e:
            return {"message": e}, 500

    @classmethod
    def delete(cls, code: str):
        store = OrderModel.find_by_code(code)
        if store:
            store.delete_from_db()
            return {"message": "store_deleted"}, 200

        return {"message": "store_not_found"}, 404


class Orders(Resource):
    @classmethod
    def get(cls):
        return {"data": order_list_schema.dump(OrderModel.find_all())}, 200

    @classmethod
    def post(cls):
        from api.order.schemas.Order import OrderSchemaSave
        body = request.get_json()
        schema = OrderSchemaSave()

        schema.load(body)
        instance = OrderModel(**schema.dump(body))
        instance.save_to_db()
        return order_schema.dump(instance), 201
