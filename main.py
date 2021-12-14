import uuid
from datetime import datetime

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/discounts.db"
api = Api(app)
db = SQLAlchemy(app)


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discount_code = db.Column(db.String(80), unique=True, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    is_used = db.Column(db.Boolean(), default=False)


def get_company(company_id):
    return {"company_id": 1}


class DiscountCode(Resource):
    discount_parser = reqparse.RequestParser()
    discount_parser.add_argument("company_id", type=int, required=True)
    discount_parser.add_argument("user_id", type=int, required=True)

    def post(self):
        # ToDo check if user have already got a discount from the company
        args = DiscountCode.discount_parser.parse_args()
        get_company(args["company_id"])  # check that the company exists
        new_code = Discount(
            discount_code=uuid.uuid4().hex,
            user_id=args["user_id"],
            company_id=args["company_id"],
        )
        db.session.add(new_code)
        db.session.commit()
        return {"discount_code": new_code.discount_code}


class UsersSharedData(Resource):
    users_shared_data_parser = reqparse.RequestParser()
    users_shared_data_parser.add_argument("company_id", type=int, required=True)

    def get(self):
        args = UsersSharedData.users_shared_data_parser.parse_args()
        rows = db.session.query(
            Discount.user_id,
        ).distinct(Discount.user_id).filter(
            Discount.company_id == args["company_id"],
        ).all()
        return {"user_ids": [row.user_id for row in rows]}


api.add_resource(DiscountCode, "/discount_code")
api.add_resource(UsersSharedData, "/users_shared_data")

if __name__ == "__main__":
    app.run(debug=True)
