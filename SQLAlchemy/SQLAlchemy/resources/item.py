import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!!"
        )
    @jwt_required()
    def get(self,name):
        row = ItemModel.find_by_name(name)
        if row:
            return row.json(),200 
        else: return {'message':'Item not found'}

    # @classmethod
    # def find_by_name(cls,name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     row = cursor.execute("select * from items where name=?",(name,))
    #     #item = next(filter(lambda x : x['name'] == name,items),None)
    #     row = row.fetchone()
    #     return row

    def post(self,name):
        if ItemModel.find_by_name(name):
            return 'Item with name {} already exist'.format(name),400 ### Bad Request
        data = Items.parser.parse_args()
        new_item = ItemModel(name,data['price'])
        try:
            new_item.save_to_db()
        except:
            return {'message':'Error occured while inserting the item'},500
        return new_item.json(),201


    def delete(self,name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "Delete from items where name=?"
        # cursor.execute(query,(name,))
        # connection.commit()
        # connec/tion.close()
        # global items
        # items = list(filter(lambda x:x['name'] != name,items))
        item  = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_fromn_db()
        return {'item':'deleted'}

    def put(self,name):
        data = Items.parser.parse_args()
        #item = next(filter(lambda x:x['name']==name,items),None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name,data['price'])
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        if item:
            item.price = data['price']
            # query = "UPDATE items set price=? where name=?"
            # cursor.execute(query,(data['price'],name))
        else:
            item = ItemModel(name,data['price'])
        item.save_to_db()
        return item.json()

            


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * from items"
        result = cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()
        return items
