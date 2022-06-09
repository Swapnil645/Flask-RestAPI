from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from user import UserRegister
from item import ItemList,Items

from security import authenticate,identity

app = Flask(__name__)
app.secret_key='jose'
api = Api(app)


jwt = JWT(app,authenticate,identity)
#jwt creates a new api with path /auth

# jwt sends username and password to authenticate it and returns the user
# The auth endpoint returns the JWT token and calls identity. 
# The token gets the userid and with that 
# it gets the correct user for which it was authenticated.


#Api works with resource and every resource has to be class

api.add_resource(Items,'/item/<string:name>')
api.add_resource(ItemList,'/item')
api.add_resource(UserRegister,'/userregister')

app.run(port=5000,debug=True)