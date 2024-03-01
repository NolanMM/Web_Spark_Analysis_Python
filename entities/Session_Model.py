from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

Session_app = Flask(__name__)
Session_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SparkWeb.db'
Session_db = SQLAlchemy(Session_app)


class Session(Session_db.Model):
    id = Session_db.Column(Session_db.Integer, primary_key=True)
    session_id = Session_db.Column(Session_db.String(40), unique=True)
    date_created = Session_db.Column(Session_db.DateTime, default=datetime.utcnow)
    is_logged_in = Session_db.Column(Session_db.Boolean, default=False)
    remember_me = Session_db.Column(Session_db.Boolean, default=False)
    session_id_expires_at = Session_db.Column(Session_db.DateTime, default=datetime.utcnow)

    def __init__(self, session_id, date_created, is_logged_in, remember_me, session_id_expires_at):
        self.session_id = session_id
        self.date_created = date_created
        self.is_logged_in = is_logged_in
        self.remember_me = remember_me
        self.session_id_expires_at = session_id_expires_at

    def __repr__(self):
        return '<Session %r>' % self.session_id