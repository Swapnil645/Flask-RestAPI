from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required

from security import authenticate,identity

app = Flask(__name__)
app.secret_key='jose'
api = Api(app)
items = []

jwt = JWT(app,authenticate,identity)
#jwt creates a new api with path /auth

# jwt sends username and password to authenticate it and returns the user
# The auth endpoint returns the JWT token and calls identity. 
# The token gets the userid and with that 
# it gets the correct user for which it was authenticated.


#Api works with resource and every resource has to be class

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!!"
        )
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x : x['name'] == name,items),None)
        return {'item':item},200 if item else 404

    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return 'Item with name {} already exist'.format(name),400 ### Bad Request
        data = Items.parser.parse_args()
        new_item = {'name':name,'price':data['price']}
        items.append(new_item)
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

api.add_resource(Items,'/item/<string:name>')
api.add_resource(ItemList,'/item')

app.run(port=5000,debug=True)