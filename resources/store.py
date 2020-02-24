from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# Model
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="Name is required"
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store doens't exist"}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return 'Store was deleted', 200
        return 'Store not found', 404


class StoreList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="The name of the store is required"
    )

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}

    def post(self):
        # * data {name:}
        data = StoreList.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {"message": f"The store {data['name']} already exists"}

        store = StoreModel(data['name'])
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating new store"}, 500

        return store.json(), 201
