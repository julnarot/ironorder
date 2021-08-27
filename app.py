from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from marshmallow import ValidationError
# from dotenv import load_dotenv

from db import db
from ma import ma
from api.order.resources.Order import Order, Orders

app = Flask(__name__)
CORS(app)

app.config.from_object("default_config")
api = Api(app)


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(Order, "/order/<string:code>")
api.add_resource(Orders, "/orders")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
