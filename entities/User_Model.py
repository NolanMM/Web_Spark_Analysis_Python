from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
User_app = Flask(__name__)
User_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SparkWeb.db'
User_db = SQLAlchemy(User_app)


class User(User_db.Model):
    id = User_db.Column(User_db.Integer, primary_key=True)
    username = User_db.Column(User_db.String(80), unique=True)
    password = User_db.Column(User_db.String(80))
    email = User_db.Column(User_db.String(120), unique=True)
    date_created = User_db.Column(User_db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email, date_created=datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = password
        self.date_created = date_created

    def __repr__(self):
        return '<User %r>' % self.username