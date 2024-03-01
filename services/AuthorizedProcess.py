from helper.security_aes import AESCipher
from datetime import datetime, timedelta

from entities.User_Model import User, User_db, User_app
from entities.Session_Model import Session, Session_db, Session_app


class AuthorizedProcess:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def register(self, username, password, email) -> bool:
        try:
            with User_app.app_context():
                if User.query.filter_by(username=username).first():
                    return False
                else:
                    cipher = AESCipher(password)
                    encrypted_password = cipher.encrypt(password)
                    new_user = User(username=username, password=encrypted_password, email=email)
                    User_db.session.add(new_user)
                    User_db.session.commit()
            return True
        except Exception as e:
            print(f'There was an issue adding your task: {e}')
            return False

    def login(self, username, password) -> bool:
        with User_app.app_context():
            user = User.query.filter_by(username=username).first()
        if not user:
            return False
        else:
            cipher = AESCipher(password)
            encrypted_password = cipher.encrypt(password)
            if user.password == encrypted_password:
                return True
            else:
                return False


    def logout(self, session_id):
        print("Logged out successfully.")
