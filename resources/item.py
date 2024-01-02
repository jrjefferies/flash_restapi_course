import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from db import stores

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")      # http://127.0.0.1:5000/item/ITEM_ID
class Store(MethodView):
    def get(self, item_id):
        try:
            return {"item": items[item_id]}
        except KeyError:
            abort(404, message="Item not found. ")
        
    def put(self, item_id):
        item_data = request.get_json()
        if ( 
            "price" not in item_data
            or "name" not in item_data
        ):
            abort( 
                400,
                message= "Bad request. Ensure 'price', and 'name' are included in the JSON payload"
            )
        try:
            item = items[item_id] 
            items[item_id] |= item_data       # new Dict update operator
            return item, 201
        except KeyError:
            abort(404, message="Item not found. ")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found. ")



@blp.route("/item")      # http://127.0.0.1:5000/store
class Store(MethodView):
    def get(self):
        return {"item": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if ( 
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort( 
                400,
                message= "Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload"
            )
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"] 
            ):
                abort(400, message=f"Item already exists")
            
        if item_data["store_id"] not in stores:
            return {"message": "Store not found"}, 404

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201




