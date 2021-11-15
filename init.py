from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
my_db = SQLAlchemy(app)