from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

# Ressources
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

# Module created for JWT
from security import authenticate, identity

app = Flask(__name__)
# ? Optimisation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "KEKW"
api = Api(app)

# ? Execut the first time we request something -
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)


#! Add Ressources
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# ? This code execut only if we execut app.py if we import app somewhere __name__ != __main__
# if __name__ == '__main__':
db.init_app(app)
# app.run(port=5000, debug=True)
