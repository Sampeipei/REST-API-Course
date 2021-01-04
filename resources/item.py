from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): # Inherite Resource class!!
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannnot be blank!!"
            )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="This field cannnot be blank!!"
            )
    
    @jwt_required()
    def get(self, name): # Define method that resource excepts
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self,name):
        # Error first approach!!! -> Deal with error first!!!
        if ItemModel.find_by_name(name):
            return {'message', 'An item with name {} already exists.'.format(name)}, 400 # 400 show bad request!!

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal server error

        return item.json(), 201 # No need to jsonify in flask_restful. Code 201 means created. (202 is accepted)
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}