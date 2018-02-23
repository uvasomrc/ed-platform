import smtplib
import uuid
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template
import markdown2

TEST_MESSAGES = []

class Notify():
    " Loops through workshops, notifying participants of "

    def __init__(self, app):
        self.app = app
        self.api_url = app.config['API_URL']
        self.site_url = app.config['SITE_URL']

    def tracking_code(self):
        return str(uuid.uuid4())[:16]

    def email_server(self):
        server_details = '%s:%s' % (self.app.config['MAIL_SERVER'],
                                    self.app.config['MAIL_PORT'])
        print("Connecting to: " + server_details)
        server = smtplib.SMTP(server_details)

        server.ehlo()
        if (self.app.config['MAIL_USE_TLS']):
            server.starttls()

        if (self.app.config['MAIL_USERNAME']):
            server.login(self.app.config['MAIL_USERNAME'],
                         self.app.config['MAIL_PASSWORD'])

        return server

    def send_email(self, subject, recipients, text_body, html_body, sender=None, ical=None):
        msgRoot = MIMEMultipart('related')
        msgRoot.set_charset('utf8')

        if (sender == None):
            sender = self.app.config['MAIL_DEFAULT_SENDER']

        msgRoot['Subject'] = Header(subject.encode('utf-8'), 'utf-8').encode()
        msgRoot['From'] = sender
        msgRoot['To'] = ', '.join(recipients)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        part1 = MIMEText(text_body, 'plain', _charset='UTF-8')
        part2 = MIMEText(html_body, 'html', _charset='UTF-8')

        msgAlternative.attach(part1)
        msgAlternative.attach(part2)

        if(ical):
            ical_atch = MIMEText(ical.decode("utf-8"),'calendar')
            ical_atch.add_header('Filename','event.ics')
            ical_atch.add_header('Content-Disposition','attachment; filename=event.ics')
            msgRoot.attach(ical_atch)

        if ('TESTING' in self.app.config and self.app.config['TESTING']):
            print("TEST:  Recording Emails, not sending")
            TEST_MESSAGES.append(msgRoot)
            return

        if (self.app.config['DEVELOPMENT']):
            print("DEVELOP:  Sending All emails to " + self.app.config['MAIL_DEFAULT_RECIPIENT'])
            recipients = [self.app.config['MAIL_DEFAULT_RECIPIENT']]

        server = self.email_server()
        server.sendmail(sender, recipients, msgRoot.as_bytes())
        server.quit()


    def registered(self, participant, session):

        subject = "CADRE Academy: Registration Successful"
        tracking_code = self.tracking_code()

        text_body = render_template("register_email.txt",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url)

        html_body = render_template("register_email.html",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    tracking_code=tracking_code)

        self.send_email(subject,
                          recipients=[participant.email_address], text_body=text_body,
                          html_body=html_body, ical=session.ical())

        return tracking_code

    def message_to_attendees(self, instructor, content, participant, session, subject):

        subject = "CADRE Academy: " + subject
        tracking_code = self.tracking_code()
        html_content = markdown2.markdown(content)

        text_body = render_template("instructor_message.txt",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=instructor, content=content)
        html_body = render_template("instructor_message.html",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=instructor, content=html_content,
                                    tracking_code=tracking_code)

        self.send_email(subject,
                          recipients=[participant.email_address], text_body=text_body,
                          html_body=html_body)

        return tracking_code

    def message_to_followers(self, instructor, content, participant, workshop, subject):

        subject = "CADRE Academy: " + subject
        tracking_code = self.tracking_code()
        html_content = markdown2.markdown(content)

        text_body = render_template("instructor_to_followers.txt",
                                    workshop=workshop, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=instructor, content=content)
        html_body = render_template("instructor_to_followers.html",
                                    workshop=workshop, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=instructor, content=html_content,
                                    tracking_code=tracking_code)

        self.send_email(subject,
                          recipients=[participant.email_address], text_body=text_body,
                          html_body=html_body)

        return tracking_code

    def message_confirm(self, session, participant):

        subject = "CADRE Academy: Upcoming Workshop"
        tracking_code = self.tracking_code()

        text_body = render_template("confirm_email.txt",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=session.workshop.instructor,
                                    tracking_code=tracking_code)
        html_body = render_template("confirm_email.html",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=session.workshop.instructor,
                                    tracking_code=tracking_code)

        self.send_email(subject,
                          recipients=[participant.email_address], text_body=text_body,
                          html_body=html_body)

        return tracking_code

    def message_followers_seats_open(self, session, participant, new_session):
        '''Sends a message intended for followers that seats are available in an upcoming session for a workshop they follow.'''
        subject = "CADRE Academy: Upcoming Workshop"
        tracking_code = self.tracking_code()

        text_body = render_template("seats_open.txt",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=session.workshop.instructor,
                                    tracking_code=tracking_code,
                                    new_session=new_session)
        html_body = render_template("seats_open.html",
                                    session=session, participant=participant,
                                    api_url=self.api_url, site_url=self.site_url,
                                    instructor=session.workshop.instructor,
                                    tracking_code=tracking_code,
                                    new_session=new_session)

        self.send_email(subject,
                          recipients=[participant.email_address], text_body=text_body,
                          html_body=html_body)

        return tracking_code