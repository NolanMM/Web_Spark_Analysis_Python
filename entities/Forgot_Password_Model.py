from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

ForgotPassword_app = Flask(__name__)
ForgotPassword_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SparkWeb.db'
ForgotPassword_db = SQLAlchemy(ForgotPassword_app)


class ForgotPasswordRecord(ForgotPassword_db.Model):
    id = ForgotPassword_db.Column(ForgotPassword_db.Integer, primary_key=True)
    username = ForgotPassword_db.Column(ForgotPassword_db.String(40), default="")
    email = ForgotPassword_db.Column(ForgotPassword_db.String(40))
    verification_code = ForgotPassword_db.Column(ForgotPassword_db.String(10), default="")
    link_reset = ForgotPassword_db.Column(ForgotPassword_db.String(40), default="")
    date_created = ForgotPassword_db.Column(ForgotPassword_db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, verification_code, link_reset, date_created):
        self.username = username
        self.date_created = date_created
        self.email = email
        self.verification_code = verification_code
        self.link_reset = link_reset

    def __repr__(self):
        return '<Session %r>' % self.username