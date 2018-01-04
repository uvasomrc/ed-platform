import datetime
import socket

import sys
from flask_script import Command, Option, Manager, prompt_bool
from flask import current_app

from ed_platform import models, db

#class Confirmation(Command):

#    """Loops through workshops, notifying participants of various events """

#    def __init__(self, app):
#        object.__init__(self)
#        self.notifier = Notify(app)

#    def run(self):
#        print("I'm gonna notify some folks.")
from ed_platform import Notify


def sub_opts(app, **kwargs):
    pass
manager = Manager(sub_opts, usage="Send Automated Email Messages")

@manager.command
def confirmation():
    "Asks participants to confirm their attendance in upcoming sessions"
    days_out = 3

    # Get a list of all sessions that occur in the next x days
    now = datetime.datetime.now()
    three_days_out = now + datetime.timedelta(days=days_out)
    sessions = models.Session.query.filter(models.Session.date_time.between(now, three_days_out))

    for s in sessions:

        print("Checking session " + str(s.date_time))
        print("Confirmation Sent:" + str(s.confirmation_sent()))
        if not s.confirmation_sent():
            send_confirmation(s)

@manager.command
def followers_seats_open():
    "Asks participants to confirm their attendance in upcoming sessions"
    days_out = 2

    # Get a list of all sessions that occur in the next x days
    now = datetime.datetime.now()
    three_days_out = now + datetime.timedelta(days=days_out)
    sessions = models.Session.query.filter(models.Session.date_time.between(now, three_days_out))

    for s in sessions:
        print("Checking session " + str(s.date_time))
        print("Follower Notification Sent:" + str(s.followers_notified()))
        print("Is the Session Full?:" + str(s.is_full()))
        if not s.followers_notified() and not s.is_full():
            send_followers_seats_open(s)

@manager.command
def test_followers():
    participant = models.Participant.query.filter_by(uid='dhf8r').first()
    session = models.Session.query.all()[0]
    session.workshop.followers.append(participant)
    notifier = Notify(current_app)
    tracking_code = notifier.message_followers_seats_open(session, participant)
    email_log = models.EmailLog(participant=participant,
                                    type=models.EmailMessage.TYPE_NOTIFY_FOLLOWERS,
                                    session_id=session.id,
                                    workshop_id=session.workshop.id,
                                    tracking_code=tracking_code)
    db.session.add(email_log)
    db.session.commit()

def send_confirmation(session):
    notifier = Notify(current_app)
    email = models.EmailMessage(type=models.EmailMessage.TYPE_CONFIRM,
                                session_id = session.id,
                                workshop_id = session.workshop_id,
                                subject = "Reminder Email",
                                content = "An automatic reminder email message, sent a few days before the class will begin.")
    tracking_code = "unknown"
    error = ""
    for participant_session in session.participant_sessions:
        participant = participant_session.participant
        try:
            tracking_code = notifier.message_confirm(session, participant)
        except socket.error as e:
            error = "Could not connect to SMTP server"
        except:
            error =  sys.exc_info()[0]
        finally:
            email_log = models.EmailLog(participant=participant,
                                    type=models.EmailMessage.TYPE_CONFIRM,
                                    session_id=session.id,
                                    tracking_code=tracking_code,
                                    error=error)
        email.logs.append(email_log)

    db.session.add(email)
    db.session.commit()

def send_followers_seats_open(session):
    notifier = Notify(current_app)
    email = models.EmailMessage(type=models.EmailMessage.TYPE_NOTIFY_FOLLOWERS,
                                session_id = session.id,
                                workshop_id = session.workshop_id,
                                subject = "Session Available",
                                content = "An automatic email message, sent to followers if an upcoming session has open seats")
    tracking_code = "unknown"
    error = ""
    for participant in session.workshop.followers:
        try:
            tracking_code = notifier.message_followers_seats_open(session, participant)
        except socket.error as e:
            error = "Could not connect to SMTP server"
        except:
            error =  sys.exc_info()[0]
        finally:
            email_log = models.EmailLog(participant=participant,
                                    type=models.EmailMessage.TYPE_NOTIFY_FOLLOWERS,
                                    session_id=session.id,
                                    workshop_id=session.workshop.id,
                                    tracking_code=tracking_code,
                                    error=error)
        email.logs.append(email_log)

    db.session.add(email)
    db.session.commit()
