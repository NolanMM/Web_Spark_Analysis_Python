from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

History_app = Flask(__name__)
History_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SparkWeb.db'
History_db = SQLAlchemy(History_app)


class HistoryRecord(History_db.Model):
    id = History_db.Column(History_db.Integer, primary_key=True)
    username = History_db.Column(History_db.String(40))
    date_created = History_db.Column(History_db.DateTime, default=datetime.utcnow)
    channel_id = History_db.Column(History_db.String(40), default="")
    channel_name = History_db.Column(History_db.String(40), default="")
    data = History_db.Column(History_db.Text, default="")

    def __init__(self, username, date_created, channel_id, channel_name, data):
        self.username = username
        self.date_created = date_created
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.data = data

    def __repr__(self):
        return '<Session %r>' % self.username