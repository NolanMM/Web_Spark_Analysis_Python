from entities.Forgot_Password_Model import ForgotPassword_app, ForgotPassword_db
from entities.User_Model import User, User_db, User_app
from entities.Session_Model import Session, Session_db, Session_app


# Clear data from User table
with User_app.app_context():
    User.query.delete()
    User_db.session.commit()
    print("Data cleared from User table.")

# Clear data from Session table
with Session_app.app_context():
    Session.query.delete()
    Session_db.session.commit()
    print("Data cleared from Session table.")


with ForgotPassword_app.app_context():
    ForgotPassword_db.delete()
    ForgotPassword_db.session.commit()
    print("Data cleared from ForgotPassword table.")
