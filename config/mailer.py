from config.config import HOST, USERNAME, PASSWORD, PORT
from config.schemas import MailSchema
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

def send_mail(data: dict|None=None):
    msg = MailSchema(**data)
    message = MIMEText(msg.body, 'html')
    message['From'] = USERNAME
    message['To'] = ','.join(msg.to)
    message['Subject'] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()

        return {'status': 200, 'message': 'email send successfull'}
    except Exception as e:
        return {'status': 500, 'error': e}

