import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema #, TagUpdateSchema


blp = Blueprint("tags", __name__, description="Operations on Tags")

@blp.route("/store/<int:store_id>/tag")
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

@blp.route("/tag/<int:tag_id>")      # http://127.0.0.1:5000/item/ITEM_ID
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    #this route is decorated with multiple response decorators
    @blp.response( 202, description="Deletes a tag if no item is tagged with it", example={"message" "Tag deleted."})
    @blp.alt_response(404, description="Tag not found.") 
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items.  In this case, the tag is not deleted")                       
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag Deleted"}
        abort(
            400,
            message="Could not delte tag. Make sure tag is not associated with any item, then try again.", 
        )



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



@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking")

        item.tags.append(tag)    # this does the secondary table work in the background

        try:          
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while tagging the item. {e}")

        return item    
    
    @blp.response(201, TagAndItemSchema)
    def delete(self,  item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)    # this does the secondary table work in the background

        try:
            
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while untagging the item. {e}")

        return{"message": "Item removed from tag", "item": item, "tag": tag  }   