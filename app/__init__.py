
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

headers = {
    'x-rapidapi-key': "e3667c90fdmsh083940b7f622505p123ae9jsn2ce8c2c193c7",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }


app = Flask(__name__)
app.secret_key = "D5G6A1CZ3"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import views
