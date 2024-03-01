from entities.User_Model import User, User_db,User_app
from entities.Session_Model import Session, Session_db,Session_app

with User_app.app_context():
    User_db.create_all()
    User_db.session.commit()

with Session_app.app_context():
    Session_db.create_all()
    Session_db.session.commit()

