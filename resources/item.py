
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")      # http://127.0.0.1:5000/item/ITEM_ID
class Item(MethodView):
    @jwt_required()            #means the flask need a JWT token in the auth header
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)              #Order of decorators matters, in this case the arguments comes first the response later
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):   #Note arguments marshmallow data comes before the routes data
        
        
        item = ItemModel.query.get(item_id)
        if item:     # idempotent (will create new item)
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
    
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted"}



@blp.route("/item")      # http://127.0.0.1:5000/store
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)     #fresh token required
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)

        try: 
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while inserting the item. {e}")

        return item




