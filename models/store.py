from db import db


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # ? When we use lazy = 'dynamic' it optimises the code otherwise pyhton create an object with the list of items for every store created. By doing so : self.items becomes a query builder that can look into ItemModel
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # ? Since self.items became a query builder we have to use the method .all to acces all the items
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # * This method work for update and insert
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
