from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from routes.auth import auth

app = Flask(__name__)
MySQL(app)
CORS(app)
JWTManager(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jwt'
app.config["JWT_SECRET_KEY"] = "super-secret"


app.register_blueprint(auth)

