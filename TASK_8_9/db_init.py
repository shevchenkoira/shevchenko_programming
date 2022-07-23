from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

REST = Flask("restful_api")
REST.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'
REST.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv("MY_DB_LOGIN")}:{os.getenv("MY_DB_PASSWORD")}@localhost/restfuldb'
REST.config['SQLALCHEMY_ECHO'] = True
REST.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(REST)

