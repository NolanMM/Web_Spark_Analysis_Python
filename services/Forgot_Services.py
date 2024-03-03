import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

from entities.Forgot_Password_Model import ForgotPassword_app, ForgotPasswordRecord, ForgotPassword_db
from entities.User_Model import User, User_db, User_app
from helper.Prepare_Email_Template import get_email_template_forgot_password

owner_email_address = "group1databaseservicesnolanm@gmail.com"
owner_email_password = "lazslzusaxooyirr"


def check_verification_code(code_input_, user_name):
    with ForgotPassword_app.app_context():
        record_ = ForgotPasswordRecord.query.filter_by(verification_code=code_input_, username=user_name).first()
    if record_.date_created > datetime.utcnow() - timedelta(minutes=30):
        return record_, True
    else:
        return None, False


class ForgotPasswordService:

    def __init__(self):
        self.email = ""
        self.username = ""
        self.link_reset = "https://webanalysisspark-6b94ca80dba0.herokuapp.com/ForgotPasswordEmail"
        self.verification_code = ""

    def get_email_by_username(self, user_name):
        self.username = user_name
        with User_app.app_context():
            user_check = User.query.filter_by(username=self.username).first()
        if user_check is not None:
            self.email = user_check.email
            self.verification_code = generate_verification_code()
            self.link_reset = self.link_reset + "?code=" + self.verification_code + "&username=" + self.username
            with ForgotPassword_app.app_context():
                new_forgot_password = ForgotPasswordRecord(self.username,
                                                           self.email,
                                                           self.verification_code,
                                                           self.link_reset,
                                                           datetime.utcnow())
                ForgotPassword_db.session.add(new_forgot_password)
                ForgotPassword_db.session.commit()
            return True
        else:
            return None


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(secrets.choice(characters) for i in range(length))
    return verification_code


class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.email_address = owner_email_address
        self.password = owner_email_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_verification_email(self,recipient_username, recipient_email, verification_code, verification_link):
        msg = MIMEMultipart()
        msg['From'] = "NolanM - Youtube Analysis Web Page"
        msg['To'] = recipient_email
        msg['Subject'] = 'Email Verification Code'

        body = get_email_template_forgot_password(recipient_username, verification_code, verification_link)

        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.password)
                server.send_message(msg)
                server.quit()
            return True
        except Exception as e:
            return False


# if __name__ == "__main__":
#
#     username = "Minh Nguyen"
#
#     email_service = EmailService()
#     email = "minhlenguyen02@gmail.com"
#     verification_code = generate_verification_code()
#     link_reset = "https://webanalysisspark-6b94ca80dba0.herokuapp.com/ForgotPassword?code=" + verification_code
#
#     is_sent = email_service.send_verification_email(username, email, verification_code, link_reset)
#
#     print(is_sent)

