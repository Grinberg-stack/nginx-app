from flask import Flask, request, make_response  # Import Flask and utilities for handling requests and responses
import mysql.connector  # MySQL connector for database communication
import os  # For accessing environment variables
import socket  # For retrieving internal server IP

app = Flask(__name__)  # Create Flask application instance

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),  # Get MySQL host from environment variables (default: 'db')
        user=os.getenv('MYSQL_USER', 'user'),  # Get MySQL user from environment variables
        password=os.getenv('MYSQL_PASSWORD', 'password'),  # Get MySQL password from environment variables
        database=os.getenv('MYSQL_DB', 'app_db')  # Get MySQL database name from environment variables
    )

def update_counter():
    conn = get_db_connection()  # Connect to MySQL
    cursor = conn.cursor()  # Create a cursor to execute SQL queries
    cursor.execute('UPDATE counter SET count = count + 1 WHERE id=1')  # Increase counter by 1
    conn.commit()  # Save changes to database
    cursor.close()  # Close cursor
    conn.close()  # Close connection

def get_counter():
    conn = get_db_connection()  # Connect to MySQL
    cursor = conn.cursor()  # Create cursor
    cursor.execute('SELECT count FROM counter WHERE id=1')  # Get the current counter value
    count = cursor.fetchone()[0]  # Fetch the first result
    cursor.close()  # Close cursor
    conn.close()  # Close connection
    return count  # Return the counter value

@app.route('/')
def home():
    update_counter()  # Increment counter
    client_ip = request.remote_addr  # Get client IP address
    internal_ip = socket.gethostbyname(socket.gethostname())  # Get internal server IP
    stored_rep_ip = request.cookies.get('REP_IP', internal_ip)  # Retrieve stored replica IP from cookie (or default to internal IP)
    
    conn = get_db_connection()  # Connect to MySQL
    cursor = conn.cursor()  # Create cursor
    cursor.execute('INSERT INTO access_log (client_ip, internal_ip) VALUES (%s, %s)', (client_ip, stored_rep_ip))  # Log access details
    conn.commit()  # Save changes
    cursor.close()  # Close cursor
    conn.close()  # Close connection
    
    resp = make_response(f'Replica IP: {stored_rep_ip}')  # Create response with replica IP
    resp.set_cookie('REP_IP', internal_ip, max_age=300)  # Set cookie with server IP (valid for 5 minutes)
    return resp  # Return response

@app.route('/showcount')
def show_count():
    return f'Global counter: {get_counter()}'  # Return the current counter value

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run Flask server on all interfaces (port 5000)