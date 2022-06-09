from crypt import methods
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

stores = [
    {
        'name': 'Dreamer stores',
        'items': [
            {
               'name':'candy',
               'price':5 
            }

        ]
    }
]

#post store/ data{name:}
#get  store/string:name 
#get store/
#post store/string:name/item {name,price}
#get store/string:name/item
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store',methods=['POST'])
def create_store():
    request_date = request.get_json()
    new_store = {'name':request_date['name'],'items':[]}
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>')
def get_store1(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':'No Match Found'})
    


@app.route('/store')
def get_store():
    return jsonify({'stores':stores})


@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    request_date = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {'name':request_date['name'],
            'price':request_date['price']}
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'No Match Found'})



@app.route('/store/<string:name>/item',methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify(store['items'])


app.run(port=5000)


