import datetime
import uuid

import jwt

from ed_platform import app, db, ma, RestException


class User():
    '''Used exclusively to manage the SSO/Shibboleth information,
       Participants are the actual users returned from the API.'''
    uid = ""
    givenName = ""
    email = ""
    surName = ""
    affiliation = ""
    displayName = ""
    eppn = ""
    title = ""

    def __init__(self, uid, givenName, email, surName, affiliation,
                 displayName, eppn, title):
        uid = uid
        givenName = givenName
        email = email
        surName = surName
        affiliation = affiliation
        displayName = displayName
        eppn = eppn
        title = title


class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    track_workshops = db.relationship('TrackWorkshop', backref='track')

    def __init__(self, image_file, title, description):
        self.image_file = image_file
        self.title = title
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Workshop(db.Model):
    __tablename__ = 'workshop'

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    track_workshops = db.relationship('TrackWorkshop', backref='workshop')
    sessions = db.relationship("Session", backref="workshop")

class TrackWorkshop(db.Model):
    __tablename__ = 'track_workshop'
    track_id = db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True)
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'), primary_key=True)
    order = db.Column(db.Integer)

class Participant(db.Model):
    __tablename__ = 'participant'
    id  = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String())
    display_name = db.Column(db.String())
    email_address = db.Column(db.String())
    phone_number = db.Column(db.String())
    bio = db.Column(db.TEXT())
    image_file = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_sessions = db.relationship('ParticipantSession', backref='participant')
    email_logs = db.relationship('EmailLog', backref='participant')
    sent_emails = db.relationship('EmailMessage', backref='author')

    def is_registered(self, session):
        return len([r for r in self.participant_sessions if r.session_id == session.id]) > 0

    def register(self, session, is_instructor=False):
        if(self.is_registered(session)): return
        self.participant_sessions.append(ParticipantSession(
            participant_id = self.id, session_id=session.id, is_instructor=is_instructor
        ))

    def getParticipantSession(self, session):
        if(not self.is_registered(session)): return
        for ps in self.participant_sessions:
            if ps.session_id == session.id:
                return(ps)

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2, minutes=0, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': self.uid
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RestException(RestException.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise RestException(RestException.TOKEN_INVALID)

class Session(db.Model):
    """A Workshop Session or Class, but Session / Class are too common and we get conflicts as we lack a namespace, and wanted a single term. """
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    location = db.Column(db.TEXT())
    instructor_notes = db.Column(db.TEXT())
    max_attendees = db.Column(db.Integer)
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
    participant_sessions = db.relationship('ParticipantSession', backref='session')
    email_messages = db.relationship('EmailMessage', backref='session')

    def instructors(self):
        instructors = []
        for ps in self.participant_sessions:
            if ps.is_instructor:
                instructors.append(ps.participant)
        return instructors

    def participants(self):
        participants = []
        for ps in self.participant_sessions:
            if not ps.is_instructor:
                participants.append(ps)
        return participants

    def total_participants(self):
        return(len(self.participants()))

class ParticipantSession(db.Model):
    __tablename__ = 'participant_session'
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True)
    session_id = db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    review_score = db.Column(db.Integer)
    review_comment = db.Column(db.TEXT())
    attended = db.Column(db.Boolean, default=False)
    is_instructor = db.Column(db.Boolean, default=False)

class EmailMessage(db.Model):
    __tablename__ = 'email_message'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column('session_id', db.Integer, db.ForeignKey('session.id'))
    subject = db.Column(db.String())
    content = db.Column(db.TEXT())
    sent_date = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column('author_id', db.Integer, db.ForeignKey('participant.id'))
    logs = db.relationship("EmailLog", backref="email_message")

class EmailLog(db.Model):
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True)
    email_message_id = db.Column('email_message_id', db.Integer, db.ForeignKey('email_message.id'), primary_key=True)
    tracking_code = db.Column(db.String(), default=str(uuid.uuid4())[:16])
    opened = db.Column(db.Boolean, default=False)


# For marshalling objects to the database
# ----------------------------------------

class TrackDBSchema(ma.ModelSchema):
    class Meta:
        model = Track

class WorkshopDBSchema(ma.ModelSchema):
    class Meta:
        model = Workshop

class TrackWorkshopDBSchema(ma.ModelSchema):
    class Meta:
        model = TrackWorkshop

class SessionDBSchema(ma.ModelSchema):
    class Meta:
        model = Session

class ParticipantDBSchema(ma.ModelSchema):
    class Meta:
        model = Participant

class ParticipantSessionDBSchema(ma.ModelSchema):
    class Meta:
        model = ParticipantSession
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_registration',
                          participant_id='<participant.id>', session_id='<session.id>')
    },  dump_only = True)

class EmailMessageDbSchema(ma.ModelSchema):
    class Meta:
        model = EmailMessage

class EmailLogDbSchema(ma.ModelSchema):
    class Meta:
        model = EmailLog

# For marshalling objects to the Front End
# ----------------------------------------

class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid','givenName','email','surName','affiliation', 'displayName',
                  'eppn','title')
        ordered = True

class TrackAPISchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','title', 'description', '_links')
        ordered = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_track', track_id='<id>'),
        'collection': ma.URLFor('get_tracks'),
        'image': ma.URLFor('get_track_image', track_id='<id>'),
        'workshops': ma.URLFor('get_track_workshops', track_id='<id>'),
    })
#    workshops = ma.Method('links_to_workshops')
#    def links_to_workshops(self, obj):
#        return list(map(lambda t: flask.url_for('get_workshop', id=t.workshop_id),
#                                                obj.track_workshops))

class ParticipantAPIMinimalSchema(ma.Schema):
    class Meta:
        fields = ('id','display_name', 'bio', '_links')
        order = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'image': ma.URLFor('get_participant_image', id='<id>'),
    })

class WorkshopAPIMinimalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', '_links')
        ordered = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_workshop', id='<id>'),
        'collection': ma.URLFor('get_workshops'),
        'image': ma.URLFor('get_workshop_image', id='<id>'),
        'tracks': ma.URLFor('get_workshop_tracks', id='<id>'),
        'sessions': ma.URLFor('get_workshop_sessions', id='<id>'),
    })

class SessionAPIMinimalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date_time','duration_minutes','instructor_notes','max_attendees', 'workshop')
        ordered = True
    workshop = ma.Nested(WorkshopAPIMinimalSchema)
#    instructors = ma.Nested(ParticipantAPIMinimalSchema)


class ParticipantSessionAPISchema(ma.Schema):
    class Meta:
        fields = ('participant', 'session', 'created', 'review_score', 'review_comment', 'attended', 'is_instructor')
        ordered = True
    participant = ma.Nested(ParticipantAPIMinimalSchema)
    session = ma.Nested(SessionAPIMinimalSchema)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'sessions': ma.URLFor('get_participant_sessions', id='<id>')
    })

class SessionAPISchema(ma.Schema):
    class Meta:
        fields = ('id', 'date_time', 'duration_minutes', 'instructor_notes',
                  'workshop', '_links', 'max_attendees', 'participants', 'instructors')
        ordered = True
    participants = ma.List(ma.Nested(ParticipantSessionAPISchema))
    workshop = ma.Nested(WorkshopAPIMinimalSchema)
    instructors = ma.List(ma.Nested(ParticipantAPIMinimalSchema))

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_session', id='<id>'),
        'collection': ma.URLFor('get_sessions'),
        'workshop': ma.URLFor('get_workshop', id='<workshop_id>'),
        'register': ma.URLFor('register', id='<id>'),
    })

class WorkshopAPISchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', '_links', 'sessions')
        ordered = True
    sessions = ma.List(ma.Nested(SessionAPISchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_workshop', id='<id>'),
        'collection': ma.URLFor('get_workshops'),
        'image': ma.URLFor('get_workshop_image', id='<id>'),
        'tracks': ma.URLFor('get_workshop_tracks', id='<id>'),
        'sessions': ma.URLFor('get_workshop_sessions', id='<id>'),
    })




class ParticipantAPISchema(ma.Schema):


    class SubAttendSchema(ma.Schema):
        class SubSessionSchema(ma.Schema):
            class Meta:
                fields = ('id', 'date_time', 'duration_minutes', 'instructor_notes', 'max_attendees', 'workshop',
                          'total_participants', 'instructors', '_links')
                ordered = True
            workshop = ma.Nested(WorkshopAPIMinimalSchema)
            instructors = ma.List(ma.Nested(ParticipantAPIMinimalSchema))
            _links = ma.Hyperlinks({
                'self': ma.URLFor('get_session', id='<id>'),
                'collection': ma.URLFor('get_sessions'),
                'workshop': ma.URLFor('get_workshop', id='<workshop_id>'),
                'register': ma.URLFor('register', id='<id>'),
            })

        class Meta:
            fields = ('session', 'created', 'review_score', 'review_comment',
                      'attended', 'is_instructor')
            ordered = True
        session = ma.Nested(SubSessionSchema) 

    class Meta:
        fields = ('id', 'uid', 'display_name', 'email_address', 'phone_number',
                  'bio', 'created', '_links', 'participant_sessions')
        ordered = True
    participant_sessions = ma.List(ma.Nested(SubAttendSchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'image': ma.URLFor('get_participant_image', id='<id>'),
        'sessions': ma.URLFor('get_participant_sessions', id='<id>')
    })


