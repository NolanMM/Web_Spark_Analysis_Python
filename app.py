import json

from flask import Flask, render_template, request, make_response, Response, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets, string
import time

from entities.History_Search_Model import History_app, History_db, HistoryRecord
from entities.User_Model import User, User_db, User_app
from entities.Session_Model import Session, Session_db, Session_app
from services.AuthorizedProcess import AuthorizedProcess
from services.Cached_Services import get_report_data, get_report_history_data
from services.Youtube_Analysis_Services import PysparkModule

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
                expires_at = datetime.now() + timedelta(days=7)
                if is_valid:
                    new_session = Session(session_id=session_id, date_created=datetime.utcnow(), is_logged_in=True, remember_me=remember_me, session_id_expires_at=expires_at)
                    try:
                        with Session_app.app_context():
                            Session_db.session.add(new_session)
                            Session_db.session.commit()
                    except Exception as e:
                        return f'There was an issue adding your account: {e}'

                    response = make_response(render_template('HomePage.html'))
                    is_cached = request.cookies.get('cached_valid')
                    if is_cached == "True":
                        response.delete_cookie('cached_valid')
                    channel_name = request.cookies.get('channel_name')
                    if channel_name is not None:
                        response.delete_cookie('channel_name')
                    response.set_cookie('username', username, expires=expires_at)
                    response.set_cookie('session_id', session_id, expires=expires_at)
                    return response
                else:
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
                            response = make_response(render_template('HomePage.html'))
                            is_cached = request.cookies.get('cached_valid')
                            if is_cached == "True":
                                response.delete_cookie('cached_valid')
                            channel_name = request.cookies.get('channel_name')
                            if channel_name is not None:
                                response.delete_cookie('channel_name')
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
                                # set cookie name username
                                response = make_response(render_template('HomePage.html'))
                                is_cached = request.cookies.get('cached_valid')
                                if is_cached == "True":
                                    response.delete_cookie('cached_valid')
                                channel_name = request.cookies.get('channel_name')
                                if channel_name is not None:
                                    response.delete_cookie('channel_name')
                                response.set_cookie('username', username, expires=expires_at)
                                with Session_app.app_context():
                                    Session_db.session.add(session)
                                    Session_db.session.commit()
                                return response
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
                            response = make_response(render_template('HomePage.html'))
                            is_cached = request.cookies.get('cached_valid')
                            if is_cached == "True":
                                response.delete_cookie('cached_valid')
                            channel_name = request.cookies.get('channel_name')
                            if channel_name is not None:
                                response.delete_cookie('channel_name')
                            response.set_cookie('username', username, expires=expires_at)
                            response.set_cookie('session_id', session_id, expires=expires_at)
                            return response
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
                        response = make_response(render_template('HomePage.html'))
                        is_cached = request.cookies.get('cached_valid')
                        if is_cached == "True":
                            response.delete_cookie('cached_valid')
                        channel_name = request.cookies.get('channel_name')
                        if channel_name is not None:
                            response.delete_cookie('channel_name')
                        return response
                    else:
                        return render_template("LoginPage.html")
                else:
                    session.is_logged_in = False
                    session.remember_me = False
                    return render_template('LoginPage.html')
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
                is_cached = request.cookies.get('cached_valid')
                if is_cached == "True":
                    response.delete_cookie('cached_valid')
                channel_name = request.cookies.get('channel_name')
                if channel_name is not None:
                    response.delete_cookie('channel_name')
                username = request.cookies.get('username')
                if username is not None:
                    response.delete_cookie('username')
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
        # reset the cookie
        response = make_response(render_template('LoginPage.html'))
        response.set_cookie('session_id', session_id, expires=expires_at)
        response.delete_cookie('username')
        response.delete_cookie('channel_name')
        response.delete_cookie('cached_valid')
        return response
    else:
        username = request.cookies.get('username')
        if username:
            response = make_response(render_template('LoginPage.html'))
            response.delete_cookie('username')
            response.delete_cookie('channel_name')
            response.delete_cookie('cached_valid')
            return response
    return render_template('LoginPage.html')


@app.route('/HomePage', methods=['POST', 'GET'])
def home_page():
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        with Session_app.app_context():
            session = Session.query.filter_by(session_id=session_id).first()
        if session:
            expires_at = session.session_id_expires_at
            if expires_at > datetime.utcnow() and session.is_logged_in:
                response = make_response(render_template('HomePage.html'))
                is_cached = request.cookies.get('cached_valid')
                if is_cached == "True":
                    response.delete_cookie('cached_valid')
                channel_name = request.cookies.get('channel_name')
                if channel_name is not None:
                    response.delete_cookie('channel_name')
                return response
            else:
                response = make_response(render_template('LoginPage.html'))
                is_cached = request.cookies.get('cached_valid')
                if is_cached == "True":
                    response.delete_cookie('cached_valid')
                channel_name = request.cookies.get('channel_name')
                if channel_name is not None:
                    response.delete_cookie('channel_name')
                return response
        else:
            response = make_response(render_template('LoginPage.html'))
            is_cached = request.cookies.get('cached_valid')
            if is_cached == "True":
                response.delete_cookie('cached_valid')
            channel_name = request.cookies.get('channel_name')
            if channel_name is not None:
                response.delete_cookie('channel_name')
            return response
    else:
        response = make_response(render_template('LoginPage.html'))
        is_cached = request.cookies.get('cached_valid')
        if is_cached == "True":
            response.delete_cookie('cached_valid')
        channel_name = request.cookies.get('channel_name')
        if channel_name is not None:
            response.delete_cookie('channel_name')
        return response


@app.route('/AnalysisChannel', methods=['GET', 'POST'])
def analysis_channel_task():
    session_id = request.cookies.get('session_id')
    if request.method == 'GET':
        if session_id is not None:
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                if expires_at > datetime.utcnow() and session.is_logged_in:
                    channel_name = request.args.get('inputchannel_name')
                    if channel_name == "" or channel_name is None:
                        return render_template('HomePage.html')
                    response = make_response(render_template('AnalysisPage.html'))
                    response.set_cookie('channel_name', channel_name, expires=expires_at)
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
                        channel_name_search = '@' + channel_name
                        username = request.cookies.get('username')
                        transformed_data,cached_valid = get_report_data(channel_name_search)
                        if transformed_data is not None:
                            pyspark_module = PysparkModule(channel_name_search)
                            channel_id = pyspark_module.get_channel_id()
                            transformed_data_to_string = json.dumps(transformed_data)
                            new_history_record = HistoryRecord(username=username, date_created=datetime.utcnow(), channel_id=channel_id, channel_name=channel_name_search, data=transformed_data_to_string)
                            with History_app.app_context():
                                History_db.session.add(new_history_record)
                                History_db.session.commit()
                            response = make_response(jsonify(transformed_data))
                            cached_valid_string = "True" if cached_valid else "False"
                            response.set_cookie('cached_valid', cached_valid_string, expires=expires_at)
                            return response
                        else:
                            return render_template('HomePage.html')
                    else:
                        return render_template('LoginPage.html')
                else:
                    return render_template('LoginPage.html')
            else:
                return render_template('HomePage.html')
        else:
            return render_template('LoginPage.html')


@app.route('/History', methods=['GET', 'POST'])
def history():
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        if request.method == 'GET':
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                if expires_at > datetime.utcnow() and session.is_logged_in:
                    username = request.cookies.get('username')
                    if username is not None:
                        return render_template('HistoryPage.html')
                    else:
                        return render_template('HomePage.html')
                else:
                    return render_template('LoginPage.html')
            else:
                return render_template('LoginPage.html')
        else:
            username = request.cookies.get('username')
            if username is not None:
                history_data,cached_valid = get_report_history_data(username)
                if history_data is not None:
                    response = make_response(jsonify(history_data))
                    cached_valid_string = "True" if cached_valid else "False"
                    response.set_cookie('cached_valid', cached_valid_string, expires=datetime.utcnow() + timedelta(days=7))
                    response.set_cookie('username', username, expires=datetime.utcnow() + timedelta(days=7))
                    return response
                else:
                    return render_template('HomePage.html')
            else:
                return render_template('HomePage.html')


@app.route('/Analysis', methods=['GET'])
def analysis_search():
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        if request.method == 'GET':
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                username = request.cookies.get('username')
                if expires_at > datetime.utcnow() and session.is_logged_in:
                    if username is not None:
                        return render_template('AnalysisSearchPage.html')
                    else:
                        return render_template('HomePage.html')
                else:
                    return render_template('LoginPage.html')
            else:
                return render_template('LoginPage.html')
    else:
        return render_template('HomePage.html')


@app.route('/AnalysisDetails', methods=['GET', 'POST'])
def history_record_detail_page():
    session_id = request.cookies.get('session_id')
    if request.method == 'GET':
        username = request.cookies.get('username')
        if username is None:
            return render_template('HistoryPage.html')
        else:
            channel_id = request.args.get('channel_id')
            date_created = request.args.get('date_created')
            channel_name = request.args.get('channel_name')
            with Session_app.app_context():
                session = Session.query.filter_by(session_id=session_id).first()
            if session:
                expires_at = session.session_id_expires_at
                if expires_at > datetime.utcnow() and session.is_logged_in:
                    response = make_response(render_template('HistoryRecordDetailPage.html'))
                    response.set_cookie('channel_id', channel_id, expires=expires_at)
                    response.set_cookie('date_created', date_created, expires=expires_at)
                    response.set_cookie('channel_name', channel_name, expires=expires_at)
                    history_record_list, cached_valid = get_report_history_data(username)
                    if cached_valid:
                        cached_valid = "True"
                    else:
                        cached_valid = "False"
                    response.set_cookie('cached_valid', cached_valid, expires=expires_at)
                    return response
                else:
                    return render_template('HomePage.html')
            else:
                return render_template('HomePage.html')
    else:
        username = request.cookies.get('username')
        channel_id = request.cookies.get('channel_id')
        date_created = request.cookies.get('date_created')
        channel_name = request.cookies.get('channel_name')
        if username is None or channel_id is None or date_created is None:
            return render_template('HistoryPage.html')
        else:
            dt_object = datetime.strptime(date_created, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')

            history_record_list, cached_valid = get_report_history_data(username)
            if cached_valid:
                record_data = dict()
                for record in history_record_list:
                    rounded_dt = record['date_created']
                    rounded_dt = rounded_dt.replace(microsecond=0)
                    if record['channel_id'] == channel_id and str(rounded_dt) == str(formatted_date):
                        record_data.update(record['data'])
                if record_data is not None:
                    response = make_response(jsonify(record_data))
                    cached_valid_string = "True" if cached_valid else "False"
                    response.set_cookie('cached_valid', cached_valid_string, expires=datetime.utcnow() + timedelta(days=7))
                    response.set_cookie('channel_name', channel_name, expires=datetime.utcnow() + timedelta(days=7))
                    return response
                else:
                    return render_template('HistoryPage.html')
            else:
                if history_record_list is not None:
                    record_data = dict()
                    for record in history_record_list:
                        rounded_dt = record['date_created']
                        rounded_dt = rounded_dt.replace(microsecond=0)
                        if record['channel_id'] == channel_id and str(rounded_dt) == str(formatted_date):
                            record_data.update(record['data'])
                    if record_data is not None:
                        response = make_response(jsonify(record_data))
                        cached_valid_string = "True" if cached_valid else "False"
                        response.set_cookie('cached_valid', cached_valid_string, expires=datetime.utcnow() + timedelta(days=7))
                        response.set_cookie('channel_name', channel_name, expires=datetime.utcnow() + timedelta(days=7))
                        return response
                    else:
                        return render_template('HistoryPage.html')
                else:
                    return render_template('HistoryPage.html')


if __name__ == '__main__':
    app.run(debug=True)
