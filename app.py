from flask import Flask, render_template, request, make_response, Response, url_for, redirect, jsonify
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


@app.route('/HomePage', methods=['POST', 'GET'])
def home_page():
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        with Session_app.app_context():
            session = Session.query.filter_by(session_id=session_id).first()
        if session:
            expires_at = session.session_id_expires_at
            if expires_at > datetime.utcnow() and session.is_logged_in:
                return render_template('HomePage.html')
            else:
                return render_template('LoginPage.html')
        else:
            return render_template('LoginPage.html')
    else:
        return render_template('LoginPage.html')


@app.route('/AnalysisChannel', methods=['GET','POST'])
def analysis_channel():
    session_id = request.cookies.get('session_id')
    if request.method == 'GET':
        if session_id is not None:
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                if expires_at > datetime.utcnow() and session.is_logged_in:
                    channelName = request.args.get('inputchannel_name')
                    if channelName == "" or channelName is None:
                        return render_template('HomePage.html')
                    response = make_response(render_template('AnalysisPage.html'))
                    response.set_cookie('channel_name', channelName, expires=expires_at)
                    return response
                else:
                    return render_template('LoginPage.html')
            else:
                return render_template('LoginPage.html')
        else:
            return render_template('LoginPage.html')
    else:
        if session_id is not None:
            channel_name = request.cookies.get('channel_name')
            if channel_name is not None:
                with Session_app.app_context():
                    session = Session.query.filter_by(session_id=session_id).first()
                if session:
                    expires_at = session.session_id_expires_at
                    if expires_at > datetime.utcnow() and session.is_logged_in:
                        data = get_data()
                        return jsonify(data)
                    else:
                        return render_template('LoginPage.html')
                else:
                    return render_template('LoginPage.html')
            else:
                return render_template('HomePage.html')
        else:
            return render_template('LoginPage.html')


def get_data():
    table_data = [
        {
            "VideoID": "1",
            "VideoTitle": "Sample Video 1",
            "ViewCount": 1000,
            "LikeCount": 500,
            "DislikesCount": 50,
            "CommentsCount": 200,
            "AdditionalInformation": "Additional Info 1"
        },
        {
            "VideoID": "2",
            "VideoTitle": "Sample Video 2",
            "ViewCount": 2000,
            "LikeCount": 1000,
            "DislikesCount": 100,
            "CommentsCount": 400,
            "AdditionalInformation": "Additional Info 2"
        },
        {
            "VideoID": "3",
            "VideoTitle": "Sample Video 3",
            "ViewCount": 3000,
            "LikeCount": 1500,
            "DislikesCount": 200,
            "CommentsCount": 600,
            "AdditionalInformation": "Additional Info 3"
        }
    ]
    data = {
        'table_data': table_data,
        'TotalViews': 10000,
        'TotalLikes': 2000,
        'TotalDislikes': 500,
        'TotalEngagement': 1200,
        'labels': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"],
        'views': [1000, 1200, 1300, 1500, 1400, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
        'likes': [200, 220, 230, 250, 240, 260, 270, 280, 290, 300, 310, 320],
        'dislikes': [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
        'engagement': [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]
    }
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8000)