from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, static_folder=None)
CORS(app)


# -------------------- 页面路由 --------------------

@app.route('/')
def serve_index():
    return send_from_directory('html5', 'index.html')


@app.route('/history_page')
def serve_history_page():
    return send_from_directory('history', 'history.html')


# 创建数据库和表
def init_db():
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            name TEXT,
            weight REAL,
            price REAL,
            unit_price REAL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = data['name']
    weight = data['weight']
    price = data['price']
    unit_price = round(price / weight, 2)

    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('INSERT INTO records (date, name, weight, price, unit_price) VALUES (?, ?, ?, ?, ?)',
              (date, name, weight, price, unit_price))
    conn.commit()
    conn.close()

    return jsonify({'message': '记录添加成功'})


@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('SELECT date, name, weight, price, unit_price FROM records ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    records = [{'date': row[0], 'name': row[1], 'weight': row[2], 'price': row[3], 'unitPrice': row[4]} for row in rows]
    return jsonify(records)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
