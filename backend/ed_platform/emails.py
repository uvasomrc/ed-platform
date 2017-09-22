from ed_platform import mail, app
# from .decorators import async
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Some day we might want to send this without blocking.
#@async
#def send_async_email(app, msg):
#    with app.app_context():
#        mail.send(msg)

TEST_MESSAGES = []

def send_email(subject, recipients, text_body, html_body, sender = None):
    msg = MIMEMultipart('alternative')


    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    if(app.config['DEVELOPMENT']):
        print("DEVELOP:  Sending All emails to " + app.config['MAIL_DEFAULT_RECIPIENT'])
        recipients = [app.config['MAIL_DEFAULT_RECIPIENT']]

    if(sender == None):
        sender = app.config['MAIL_DEFAULT_SENDER']

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    if(app.config['TESTING']):
        TEST_MESSAGES.append(msg)
        print("TESTING:  NOT SENDING THIS EMAIL.")
        return

    server_details = '%s:%s' % (app.config['MAIL_SERVER'],
                                app.config['MAIL_PORT'])
    print("Connecting to: " + server_details)
    server = smtplib.SMTP(server_details)

    # FIXME: This is very specific to google.
    server.ehlo()
    server.starttls()
    server.login(app.config['MAIL_USERNAME'],
                 app.config['MAIL_PASSWORD'])
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
