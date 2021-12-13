import uuid

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class DiscountCode(Resource):
    def post(self):
        new_code = uuid.uuid4().hex
        return {'discount_code': new_code}


api.add_resource(DiscountCode, '/discount_code')

if __name__ == '__main__':
    app.run(debug=True)
