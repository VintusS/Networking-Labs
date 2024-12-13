import sqlite3
import sys
import threading
import socket
import random
import time
from flask import Flask, request, jsonify, send_from_directory
from threading import Lock

from Process.read import read_products
from Chat.Services.handler import start_websocket_server
from Crud.crud_operations import get_product, get_products_with_pagination, create_product, update_product_data, delete_product_data

database = './Database/products.db'
data = './App/Database/products.json'
products, columns, values = read_products(data)
lock = Lock()

app = Flask(__name__)

@app.route('/')
def index():
    return "It worked"

@app.route('/products', methods=['GET'])
def fetch_product():
    product_list = []
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=5, type=int)
    product_id = request.args.get('id', default=None, type=int) 

    if product_id is not None:
        # Fetch a single product by ID example: /products?id=1
        product = get_product(cursor, product_id, columns)
        print("PRODUCT", product_id, ":", product)
        if product:
            product_list.append(product)
        conn.close()
        return jsonify(product_list)

    else:
        # Fetch products with pagination example: /products?offset=5&limit=5
        product_list, total_count = get_products_with_pagination(cursor, columns, offset, limit)
        conn.close()
        return jsonify({
            "total_count": total_count,
            "offset": offset,
            "limit": limit,
            "products": product_list
        })

@app.route('/insert/product', methods=['POST'])
def insert_product():
    data = request.json
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    product_id = create_product(cursor, data)
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product created successfully", "product_id": product_id}), 201


@app.route('/update/product', methods=['PUT'])
def update_product():
    data = request.json
    product_id = request.args.get('id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    if not data:
        return jsonify({"error": "No data provided to update"}), 400

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    update_product_data(cursor, product_id, data)

    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated successfully", "product_id": product_id}), 200

@app.route('/delete/product', methods=['DELETE'])
def delete_product():
    product_id = request.args.get('id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    delete_product_data(cursor, product_id)

    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted successfully", "product_id": product_id}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    content = file.read().decode('utf-8')
    print("FILE CONTENT:", content)

    return jsonify({"message": "File uploaded successfully"}), 200

# ChatRoom
@app.route("/chat")
def serve_chat():
    return send_from_directory('./Chat/Front', 'chat.html')

@app.route("/style.css")
def serve_css():
    return send_from_directory('./Chat/Front', 'style.css')

@app.route("/script.js")
def serve_js():
    return send_from_directory('./Chat/Front', 'script.js')

def start_http_server():
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)


# For socket communication
def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            command, *args = message.split()
            
            with lock:
                if command.lower() == "write":
                    with open('./Database/shared_file.txt', 'a') as f:
                        data_to_write = f"Client {client_address}: {' '.join(args)}\n"
                        time.sleep(random.randint(1, 7))  # Simulate delay
                        f.write(data_to_write)
                        print(f"Written to file by {client_address}: {data_to_write.strip()}")
                
                elif command.lower() == "read":
                    time.sleep(random.randint(1, 7))  # Simulate delay
                    with open('./Database/shared_file.txt', 'r') as f:
                        content = f.read()
                        client_socket.sendall(content.encode('utf-8'))
                        print(f"Sent file content to {client_address}")
        except (ConnectionResetError, BrokenPipeError):
            break
    client_socket.close()
    print(f"Connection with {client_address} closed.")


def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 6000))
    server.listen(5)
    print("TCP server listening on port 6000")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        client_thread.start()

# Run WebSocket and HTTP servers in separate threads
websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
websocket_thread.start()

# Start TCP server in a separate thread
tcp_server_thread = threading.Thread(target=start_tcp_server, daemon=True)
tcp_server_thread.start()

start_http_server()