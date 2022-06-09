<<<<<<< HEAD
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import ItemList,Items
from db import db

from security import authenticate,identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False #This turns off flask sqlalchemy modification tracker
#and not turn off sqlalchemy  modification tracker

app.secret_key='jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
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

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000,debug=True)
=======

>>>>>>> b548eef03bfde404420fffd63b3443865266066e
