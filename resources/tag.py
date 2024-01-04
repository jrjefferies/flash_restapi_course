import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema #, TagUpdateSchema


blp = Blueprint("tags", __name__, description="Operations on Tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tag.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self,  tag_data, store_id):
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
        #     abort(400, message="A tag with tha name already exists in the store.")
        # tag = TagModel(**tag_data, store_id=store_id)
        tag = TagModel(**tag_data, store_id=store_id)
        
        try:
            
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while inserting the tag. {e}")

        return tag

@blp.route("/tag/<string:tag_id>")      # http://127.0.0.1:5000/item/ITEM_ID
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    # @blp.arguments(TagUpdateSchema)              #Order of decorators matters, in this case the arguments comes first the response later
    # @blp.response(200, TagSchema)
    # def put(self, tag_data, tag_id):   #Note arguments marshmallow data comes before the routes data
    #     tag = TagModel.query.get(item_id)
    #     if tag:     # idempotent (will create new item)
    #         tag.price = tag_data["price"]
    #         tag.name = tag_data["name"]
    #     else:
    #         tag = TagModel(tag_id, **tag_data)

    #     db.session.add(tag)
    #     db.session.commit()

    #     return tag
    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag Deleted"}



# @blp.route("/tag")      # http://127.0.0.1:5000/tag
# class ItemList(MethodView):
#     @blp.response(200, TagSchema(many=True))
#     def get(self):
#         return TagModel.query.all()

#     @blp.arguments(TagSchema)
#     @blp.response(200, TagSchema)
#     def post(self,tag_data):
#         tag = TagModel(**tag_data)

#         try: 
#             db.session.add(tag)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="An error occured while inserting the tag.")

#         return tag



