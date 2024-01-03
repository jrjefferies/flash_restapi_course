import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")      # http://127.0.0.1:5000/store/STORE_ID
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        item = StoreModel.query.get_or_404(store_id)
        return item

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
      
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}

@blp.route("/store")      # http://127.0.0.1:5000/store
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try: 
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400, message="A store with that name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the store.")

        return store





