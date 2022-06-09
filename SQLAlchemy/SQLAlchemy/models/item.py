import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__='items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self,name,price):
        self.name = name
        self.price = price

    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  # select * from items where name =name
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # row = cursor.execute("select * from items where name=?",(name,))
        # #item = next(filter(lambda x : x['name'] == name,items),None)
        # row = row.fetchone()
        # if row:
        #     return cls(*row)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "Insert into items values (?,?)"
        # cursor.execute(query,(self.name,self.price))
        # connection.commit()
        # connection.close()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()