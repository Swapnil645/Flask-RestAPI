import sqlite3

connection = sqlite3.connect('data.db')

#sqllite is slower in writing data to database

cursor = connection.cursor()

#create table in sqllite databse

create_table = "CREATE TABLE users (id int,username text,password text)"
cursor.execute(create_table)

user = [(1,'jose','asdf'),
(2,'swap','qwer')]
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.executemany(insert_query,user)

select_query = "select * from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()


