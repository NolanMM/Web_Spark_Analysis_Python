from entities.User_Model import User, User_db,User_app
from entities.Session_Model import Session, Session_db,Session_app
from entities.History_Search_Model import HistoryRecord, History_db, History_app

with User_app.app_context():
    User_db.create_all()
    User_db.session.commit()

with Session_app.app_context():
    Session_db.create_all()
    Session_db.session.commit()

with History_app.app_context():
    History_db.create_all()
    History_db.session.commit()

