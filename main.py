import random

from flask import Flask, request
from flask_restful import Api
from mysql import connector


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
    except:
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
            curs.execute(
                f'INSERT INTO products (id,name,price,quantity) values ("{sid}","{name}","{price}","{quantity}")')
            conn.commit()
            curs.execute(f'select * from products where id="{sid}"')
            result = curs.fetchone()
            num_generator = random.randint(1, 50000)
            return {
                "code": num_generator,
                "status": "Done",
                "data": result
            }
        elif request.method == "GET":
            curs.execute('select * from products')
            result = curs.fetchall()
            num_generator = random.randint(1, 50000)
            return {
                "code": num_generator,
                "status": "Done",
                "data": result
            }

    else:
        return {"error": 'cannot process'}


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
            "code": num_generator,
            "status": "Done",
            "data": result}
    elif request.method == "DELETE":
        curs.execute(f'DELETE FROM products WHERE id="{id}"')
        conn.commit()
        return {
            "code": num_generator,
            "staus": "Done"
        }
    elif request.method == "GET":
        curs.execute(f'select * from products where id="{id}"')
        result = curs.fetchone()
        return {
            "code": num_generator,
            "status": "Done",
            "data": result}


if __name__ == "__main__":
    app.run(debug=True)