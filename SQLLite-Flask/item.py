import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!!"
        )
    @jwt_required()
    def get(self,name):
        row = self.find_by_name(name)
        if row:
            return {'item':{'name':row[0],'price':row[1]}},200 
        else: return {'message':'Item not found'}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        row = cursor.execute("select * from items where name=?",(name,))
        #item = next(filter(lambda x : x['name'] == name,items),None)
        row = row.fetchone()
        return row

    def post(self,name):
        if self.find_by_name(name):
            return 'Item with name {} already exist'.format(name),400 ### Bad Request
        data = Items.parser.parse_args()
        new_item = {'name':name,'price':data['price']}

        connection =sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items values (?,?)"
        cursor.execute(query,(new_item['name'],new_item['price']))
        connection.commit()
        connection.close()
        return new_item,201

    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name'] != name,items))
        return {'item':'deleted'}

    def put(self,name):
        
        item = next(filter(lambda x:x['name']==name,items),None)
        data = Items.parser.parse_args()
        if item:
            item.update(data)
        else:
            item = {'name':name,'price':data['price']}
            items.append(item)
        return item

            


class ItemList(Resource):
    def get(self):
        return {'items':items}
