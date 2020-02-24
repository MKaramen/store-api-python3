import sqlite3
from flask_restful import Resource, reqparse

# Home made
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True,
                        help="Useranme is required")
    parser.add_argument('password', type=str, required=True,
                        help="Password is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        #! new_user = UserModel(data['username'], data['password'])
        new_user = UserModel(**data)
        new_user.save_to_db()
        return "New User created"
