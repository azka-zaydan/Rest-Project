import random
import mysql.connector.errors
from flask import Flask, request
from flask_restful import Api
from mysql import connector


# please install the requirements first

def get_db_conn():
    mydb = {
        'host': "localhost",
        'user': "root",
        'password': "1234",
        'port': 3306,
        'database': 'newrest'
    }
    try:
        c = connector.connect(**mydb)
        return c
    except mysql.connector.errors.DatabaseError:
        print("connection error")
        exit(1)


app = Flask(__name__)
api = Api(app)


@app.route('/api/products', methods=['POST', 'GET'])
def post_new_productor_show_all():
    conn = get_db_conn()
    curs = conn.cursor(dictionary=True)
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        if request.method == "POST":
            json = request.get_json()
            sid = json['id']
            name = json['name']
            price = json['price']
            quantity = json['quantity']
            try:
                curs.execute(
                    f'INSERT INTO products (id,name,price,quantity) values ("{sid}","{name}","{price}","{quantity}")')
                conn.commit()
                curs.execute(f'select * from products where id="{sid}"')
                result = curs.fetchone()
                num_generator = random.randint(1, 50000)
                return {
                    "code": 201,
                    "status": "Ok",
                    "data": result
                }
            except mysql.connector.errors.IntegrityError:
                return {"that ID already exist":409}

        elif request.method == "GET":
            curs.execute('select * from products')
            result = curs.fetchall()
            num_generator = random.randint(1, 50000)
            return {
                "code": 201,
                "status": "Ok",
                "data": result
            }

    else:
        return {"error cannot proccess": 400}


@app.route('/api/products/<string:sid>', methods=['PUT', 'DELETE', "GET"])
def update_get_delete_product_by_id(sid):
    conn = get_db_conn()
    curs = conn.cursor(dictionary=True)
    json = request.get_json()
    num_generator = random.randint(1, 50000)
    if request.method == 'PUT':
        newid = json['id']
        name = json['name']
        quantity = json['quantity']
        curs.execute(f'update products set id="{newid}", name="{name}",quantity={quantity} where id="{sid}"')
        conn.commit()
        curs.execute(f'select * from products where id="{newid}"')
        result = curs.fetchone()
        return {
            "code": 202,
            "status": "Ok",
            "data": result}
    elif request.method == "DELETE":
        curs.execute(f'DELETE FROM products WHERE id="{sid}"')
        conn.commit()
        return {
            "code": 202,
            "staus": "Ok"
        }
    elif request.method == "GET":
        curs.execute(f'select * from products where id="{sid}"')
        result = curs.fetchone()
        return {
            "code": 201,
            "status": "Ok",
            "data": result}


if __name__ == "__main__":
    app.run(debug=True)
