import requests 
from flask import Flask, jsonify, request, make_response
import jwt
from functools import wraps
import json
import os
from jwt.exceptions import DecodeError
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
port = int(os.environ.get('PORT', 5000))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
       # token = request.cookies.get('token')
       # Extract the JWT from the Authorization header instead
        auth_header = request.headers.get('Authorization')

        if auth_header:
            # The header is typically in the format "Bearer <token>"
            try:
                token = auth_header.split()[1]
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user_id = data['user_id']
            except IndexError:
                return jsonify({'message': 'Authorization token not found!'}), 401
            except DecodeError:
                return jsonify({'error': 'Authorization token is invalid'}), 401
            return f(current_user_id, *args, **kwargs)
        else:
            return jsonify({'message': 'Authorization header is missing!'}), 401
    return decorated

# API endpoint for user authentication
with open('db/users.json', 'r') as f:
    users = json.load(f)
@app.route('/auth', methods=['POST'])
def authenticate_user():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    username = request.json.get('username')
    password = request.json.get('password')
    for user in users:
        if user['username'] == username and user['password'] == password:
            token = jwt.encode({'user_id': user['id']}, app.config['SECRET_KEY'],algorithm="HS256")
            response = make_response(jsonify({'message': 'Authentication successful',
                                              'token': token}))
            # do not set the cookie, token is being sent in the rewponse above
            # response.set_cookie('token', token)
            return response, 200
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route("/")
def home():
    return "Hello, this is a Secured Flask Microservice"


BASE_URL = "https://dummyjson.com"

@app.route('/products', methods=['GET'])
@token_required
def get_products(current_user_id):
    #headers = {'Authorization': f'Bearer {request.cookies.get("token")}'}    
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code
    
    products = []
    for product in response.json()['products']:
        product_data = {
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'sku': product['sku']
        }
        products.append(product_data)

    return jsonify({'data': products}), 200 if products else 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)