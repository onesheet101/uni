from flask import Flask
from EndPoints.endpoints import setup_endpoints
from flask_jwt_extended import JWTManager
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

#Make sure to change this before pushing!
load_dotenv('Hidden/.env')
#Initialises the flask app library.
app = Flask(__name__)

try:

    db = mysql.connector.connect(
        host=os.getenv("SECRET_DB_HOST"),
        user=os.getenv("SECRET_DB_USER"),
        password=os.getenv("SECRET_DB_PSWRD"),
        database=os.getenv("SECRET_DB_DATABASE"),
        port=os.getenv("SECRET_DB_PORT"),
        ssl_ca=os.getenv("SECRET_DB_SSL_CA"),
        ssl_disabled=False
    )

    if db.is_connected():
        db_info = db.get_server_info()
        print("Connected to MySQL Server version ", db_info)

except Error as e:
    print("Error while connecting to MySQL", e)

#This sets the private key within the flask application that will be used to encode and decode jwt's.
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_FLASK_KEY") #Will import this from seperate file so it is secure.

#This starts running the flask extension on top of it
jwt = JWTManager(app)

#This passes the flask and extension objects to the endpoint functions so they can use their library methods.
setup_endpoints(app, jwt, db)

if __name__ == '__main__':
    #Starts flask
    app.run(debug=True)

#test