from flask import Flask, request, make_response
import mysql.connector
import os
import socket

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user=os.getenv('MYSQL_USER', 'user'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('MYSQL_DB', 'app_db')
    )

def update_counter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE counter SET count = count + 1 WHERE id=1')
    conn.commit()
    cursor.close()
    conn.close()

def get_counter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM counter WHERE id=1')
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

@app.route('/')
def home():
    update_counter()
    client_ip = request.remote_addr
    internal_ip = socket.gethostbyname(socket.gethostname())
    stored_rep_ip = request.cookies.get('REP_IP', internal_ip)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO access_log (client_ip, internal_ip) VALUES (%s, %s)', (client_ip, stored_rep_ip))
    conn.commit()
    cursor.close()
    conn.close()
    
    resp = make_response(f'Replica IP: {stored_rep_ip}')
    resp.set_cookie('REP_IP', internal_ip, max_age=300)
    return resp

@app.route('/showcount')
def show_count():
    return f'Global counter: {get_counter()}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)