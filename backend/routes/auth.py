from utils.db import db
from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import bcrypt
import re

auth = Blueprint('auth',__name__)

@auth.route("/login", methods=["POST"])
def login():
    a = 'Bad username or password'
    b = 'Username does not exist'
    username = request.json['username']
    password = request.json['password'].encode('utf-8')

    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    response = cursor.fetchall()

    if response is None:
        return jsonify({"msg": b}), 401

    hashed = str(response[0][3]).encode('utf-8')
    status = bcrypt.checkpw(password, hashed)

    if response and status:
        access_token = create_access_token(identity = username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": a}), 401

@auth.route("/signup", methods=["POST"])
def signup():   
    a = 'Successful registration!'
    b = 'User already registered'
    c = 'Invalid user only supports numbers'

    username = request.json['username']
    fullName = request.json['fullname']
    email = request.json['email']
    password = request.json['password']

    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s ', (username,))
    response = cursor.fetchone()

    if response:
        return jsonify({"msg": b}), 409
    elif not re.match(r'^[0-9,$]+$', username):
        return jsonify({"msg": c}), 409

    cursor.execute('INSERT INTO users VALUES (%s,%s,%s,%s)', (username,fullName,email, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())))
    db.connection.commit()
    return jsonify({"msg": a}), 200

@auth.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    current_user = get_jwt_identity()
    cursor = db.connection.cursor()
    cursor.execute('SELECT users.username, users.fullname, users.email FROM users WHERE username = %s', (current_user,))
    response = cursor.fetchone()

    return jsonify(response), 200