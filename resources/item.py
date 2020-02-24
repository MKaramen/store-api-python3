from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# Homemade
from models.item import ItemModel

"""""
    Server Status :
        200 - fetch went well
        201 - Was created
        400 - Error from the user
        404 - Not found
        500 - Internal server error
        
"""""


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument(
        'name',
        type=str,
        help="Name is required"
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Store id is required"
    )

    @jwt_required()
    def get(self, name):
        #! item receives an itemModel instance
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item doens't exist"}, 404

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return 'Item deleted'
        return 'Item not found', 404

    def put(self, name):
        # * data {price:, store_id:} and name from url
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Store Id required"
    )

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

    def post(self):
        # * data {name:, price:, store_id:}
        data = ItemList.parser.parse_args()
        if ItemModel.find_by_name(data['name']):
            return {"message": f"{data['name']} already exists"}

        #! Have to return otherwise we don't return anything, if we return the function we receive the return inside it
        # item = ItemModel(name = data['name'], price = data['price'], store_id = data['store_id'])
        item = ItemModel(**data)
        try:
            item.save_to_db()
        except:
            # ? Internal server error
            return {"message": "An error occured while inserting an item"}, 500

        return item.json(), 201
