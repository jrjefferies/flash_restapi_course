from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), unique=True, nullable=False)   #nullable = can it be Null (empty), False means it must exists
    name = db.Column(db.String(80), nullable=False)   #nullable = can it be Null (empty), False means it must exists
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False) 

    store = db.relationship("StoreModel", back_populates="tag")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")