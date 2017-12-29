from flask_script import Command, Option, Manager, prompt_bool
from flask import current_app
from sqlalchemy.orm import Session

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
    print("Sending Confirmation Emails.")

    notifier = Notify(current_app)
    participant = models.Participant.query.filter_by(uid='dhf8r').first()
    session = models.Session.query.first()
    tracking_code = notifier.message_confirm(participant, participant, session)
    email_log = models.EmailLog(participant=participant,
                                type="confirmation",
                                session_id=session.id,
                                tracking_code=tracking_code)

    db.session.add(email_log)
    db.session.commit()