from db import db

# ? Insteand of sending back dictionnary we send back instance of ItemModel


class ItemModel(db.Model):
    # * SQLAlchemy setup
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # ? Precision number after the coma
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    store = db.relationship('StoreModel')
    # *

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM __tablename__ WHERE item_name=name  LIMIT 1
        return cls.query.filter_by(name=name).first()

    # * This method work for update and insert
    def save_to_db(self):
        # ? SQL Alchemy can send back the item because we definied it's properties on top of the class
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
