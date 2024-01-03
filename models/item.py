from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)   #nullable = can it be Null (empty), False means it must exists
    price = db.Column(db.Integer, unique=True, nullable=False) 
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=True, nullable=False) 
    store = db.relationship("StoreModel", back_populates="item")