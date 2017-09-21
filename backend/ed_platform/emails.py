from flask_mail import Message
from ed_platform import mail, app
from .decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body, sender = None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if('DEVELOPMENT' in app.config and app.config['DEVELOPMENT']):
        # Don't send messages to people in Development Mode.
        print ("Sending message to %s" % app.config['MAIL_DEFAULT_RECIPIENT'])
        msg.recipients = [app.config['MAIL_DEFAULT_RECIPIENT']]
    mail.send(msg)
    # Sending mail async might be useful to keep from hanging,
    # but might be better to handle this on the front end.
    # send_async_email(app, msg)
