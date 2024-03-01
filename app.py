from flask import Flask, render_template, request, make_response, Response, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets, string

from entities.User_Model import User, User_db,User_app
from entities.Session_Model import Session, Session_db,Session_app
from services.AuthorizedProcess import AuthorizedProcess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SparkWeb.db'
db = SQLAlchemy(app)


def generate_session_id(length=40):
    characters = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(characters) for i in range(length))
    return session_id


@app.route('/', methods=['POST', 'GET'])
def index():
    session_id = request.cookies.get('session_id')
    expires_at = 0
    if request.method == 'POST':
        try:
            if session_id is None:
                session_id = generate_session_id(40)
                username = request.form['usernameInput']
                password = request.form['passwordInput']
                remember_me = request.form.get('RememberMe_checkbox', False)
                if remember_me == 'on':
                    remember_me = True
                else:
                    remember_me = False

                authorized_process = AuthorizedProcess()
                is_valid = authorized_process.login(username, password)

                if is_valid:
                    expires_at = datetime.now() + timedelta(days=7)
                    new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=True, remember_me=remember_me, session_id_expires_at=expires_at)
                    try:
                        with Session_app.app_context():
                            Session_db.session.add(new_session)
                            Session_db.session.commit()
                    except Exception as e:
                        return f'There was an issue adding your account: {e}'
                    response = make_response(render_template('HomePage.html'))
                    response.set_cookie('session_id', session_id, expires=expires_at)
                    return response
                else:
                    expires_at = datetime.now() + timedelta(days=7)
                    new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=False, remember_me=False, session_id_expires_at=expires_at)
                    try:
                        with Session_app.app_context():
                            Session_db.session.add(new_session)
                            Session_db.session.commit()
                    except Exception as e:
                        return f'There was an issue adding your account: {e}'
                    response = make_response(render_template('LoginPage.html'))
                    response.set_cookie('session_id', session_id, expires=expires_at)
                    return response
            else:
                try:
                    with Session_app.app_context():
                        session = Session.query.filter_by(session_id=session_id).first()
                    if session:
                        expires_at = session.session_id_expires_at
                        if expires_at > datetime.utcnow() and session.is_logged_in:
                            return render_template('HomePage.html')
                        else:
                            username = request.form['usernameInput']
                            password = request.form['passwordInput']
                            remember_me = request.form.get('RememberMe_checkbox', False)
                            if remember_me == 'on':
                                remember_me = True
                            else:
                                remember_me = False

                            authorized_process = AuthorizedProcess()
                            is_valid = authorized_process.login(username, password)

                            if is_valid:
                                session.is_logged_in = True
                                session.remember_me = remember_me
                                with Session_app.app_context():
                                    Session_db.session.add(session)
                                    Session_db.session.commit()
                                return render_template('HomePage.html')
                            else:
                                session.is_logged_in = False
                                session.remember_me = False
                                with Session_app.app_context():
                                    Session_db.session.add(session)
                                    Session_db.session.commit()
                                return render_template('LoginPage.html')
                    else:
                        expires_at = datetime.now() + timedelta(days=7)
                        username = request.form['usernameInput']
                        password = request.form['passwordInput']
                        remember_me = request.form.get('RememberMe_checkbox', False)
                        if remember_me == 'on':
                            remember_me = True
                        else:
                            remember_me = False

                        authorized_process = AuthorizedProcess()
                        is_valid = authorized_process.login(username, password)

                        if is_valid:
                            new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=True, remember_me=remember_me, session_id_expires_at=expires_at)
                            try:
                                with Session_app.app_context():
                                    Session_db.session.add(new_session)
                                    Session_db.session.commit()
                            except Exception as e:
                                return f'There was an issue adding your account: {e}'
                            return render_template('HomePage.html')
                        else:
                            new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=False, remember_me=False, session_id_expires_at=expires_at)
                            with Session_app.app_context():
                                Session_db.session.add(new_session)
                                Session_db.session.commit()
                            return render_template('LoginPage.html')
                except Exception as e:
                    return f'There was an issue adding your account: {e}'
        except Exception as e:
            return f'There was an issue adding your account: {e}'
    else:
        if session_id is None:
            session_id = generate_session_id(40)
            expires_at = datetime.now() + timedelta(days=7)
            new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=False, remember_me=False, session_id_expires_at=expires_at)
            try:
                with Session_app.app_context():
                    Session_db.session.add(new_session)
                    Session_db.session.commit()
            except Exception as e:
                return f'There was an issue adding your account: {e}'
            response = make_response(render_template('LoginPage.html'))
            response.set_cookie('session_id', session_id, expires=expires_at)
            return response
        else:
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                if expires_at > datetime.utcnow():
                    if session.is_logged_in:
                        return render_template('HomePage.html')
                    else:
                        return render_template("LoginPage.html")
                else:
                    session.is_logged_in = False
                    session.remember_me = False
                    return render_template('LoginPage.html')
            else:
                expires_at = datetime.now() + timedelta(days=7)
                new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=False, remember_me = False, session_id_expires_at=expires_at)
                try:
                    with Session_app.app_context():
                        Session_db.session.add(new_session)
                        Session_db.session.commit()
                except Exception as e:
                    return f'There was an issue adding your account: {e}'
                response = make_response(render_template('LoginPage.html'))
                response.set_cookie('session_id', session_id, expires=expires_at)
                return response


@app.route('/Register', methods=['POST', 'GET'])
def register():
    session_id = request.cookies.get('session_id')
    expires_at = 0
    if request.method == 'POST':
        try:
            if session_id is None:
                session_id = generate_session_id(40)

            username = request.form['usernameInput']
            password = request.form['passwordInput']
            email = request.form['emailInput']

            authorized_process = AuthorizedProcess()
            is_registered = authorized_process.register(username, password, email)
            if is_registered:
                expires_at = datetime.now() + timedelta(days=7)
                response = make_response(render_template('LoginPage.html'))
                response.set_cookie('session_id', session_id, expires=expires_at)
                return response
            else:
                expires_at = datetime.now() + timedelta(days=7)
                response = make_response(render_template('RegisterPage.html'))
                response.set_cookie('session_id', session_id, expires=expires_at)
                return response
        except Exception as e:
            return f'There was an issue adding your task: {e}'
    else:
        if session_id is None:
            session_id = generate_session_id(40)
            expires_at = datetime.now() + timedelta(days=7)
        response = make_response(render_template('RegisterPage.html'))
        response.set_cookie('session_id', session_id, expires=expires_at)
        return response


@app.route('/Logout', methods=['POST', 'GET'])
def logout() -> Response | str:
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        with Session_app.app_context():
            session = Session.query.filter_by(session_id=session_id).first()
            if session:
                Session_db.session.delete(session)
                Session_db.session.commit()
            date_created = session.date_created
            expires_at = session.session_id_expires_at
            new_session = Session(session_id=session_id, date_created=date_created, is_logged_in=False, remember_me=False, session_id_expires_at=expires_at)
            Session_db.session.add(new_session)
            Session_db.session.commit()
        response = make_response(render_template('LoginPage.html'))
        response.set_cookie('session_id', session_id, expires=expires_at)
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)