import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

from entities.Forgot_Password_Model import ForgotPassword_app, ForgotPasswordRecord, ForgotPassword_db
from entities.User_Model import User, User_db, User_app

owner_email_address = "your_email@gmail.com"
owner_email_password = "your_password"


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
        self.link_reset = "https://webanalysisspark-6b94ca80dba0.herokuapp.com/ForgotPassword"
        self.verification_code = ""

    def get_email_by_username(self, user_name):
        self.username = user_name
        with User_app.app_context():
            user_check = User.query.filter_by(username=self.username).first()
        if user_check is not None:
            self.email = user.email
            self.verification_code = generate_verification_code()
            self.link_reset = self.link_reset + "?code=" + self.verification_code
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

    def send_verification_email(self, recipient_email, verification_code, verification_link):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient_email
        msg['Subject'] = 'Email Verification Code'

        body = f'Your verification code is: {verification_code} + {verification_link}'
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.password)
                server.send_message(msg)
                server.quit()
            return True
        except Exception as e:
            return False


if __name__ == "__main__":

    username = "user"

    email_service = EmailService()
    ForgotPasswordService = ForgotPasswordService()
    is_email_valid = ForgotPasswordService.get_email_by_username(username)

    email_service.send_verification_email(ForgotPasswordService.email,
                                          ForgotPasswordService.verification_code,
                                          ForgotPasswordService.link_reset)

    # Return a page to take the verification code from the user

    # After the user inputs the verification code
    code_input = "123456"
    record__, is_valid = check_verification_code(code_input, username)
    if is_valid:
        # Return a page to take the new password from the user

        # After the user inputs the new password
        new_password = "new_password"
        # Update the password in the database
        with User_app.app_context():
            user = User.query.filter_by(username=username).first()
            user.password = new_password
            User_db.session.commit()

        # Return a page to inform the user that the password has been updated and
        # automatically redirect to the login page

        pass
    else:
        print("The verification code is invalid or expired")


