import datetime
import uuid

import jwt

from ed_platform import app, db, ma, RestException
from marshmallow import fields, post_load
from flask import g

class User():
    '''Used exclusively to manage the SSO/Shibboleth information,
       Participants are the actual objects returned from the API.'''
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

class Search():
    query = ""
    filters = []
    total = 0
    hits = []
    facets = []
    date_restriction = ""

    def __init__(self, query="", filters=[], date_restriction=""):
        self.query = query
        self.filters = filters
        self.date_restriction = date_restriction

    def jsonFilters(self):
        jfilter = {}
        for f in self.filters:
            jfilter[f.field] = f.value

        return jfilter

class Facet():
    name = ""
    count = 0
    is_selected = False

class Filter():
    field = ""
    value = ""

    def __init__(self, field, value):
        self.field = field
        self.value = value

class TrackCode(db.Model):
    __tablename__ = 'track_code'
    track_id = db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True)
    code_id = db.Column('code_id', db.String(), db.ForeignKey('code.id'), primary_key=True)
    order = db.Column(db.Integer())
    prereq = db.Column(db.Boolean())

class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    codes = db.relationship(lambda : TrackCode, order_by=TrackCode.order,
        backref=db.backref('track', lazy=True, cascade="all, delete-orphan", single_parent=True))

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
    sessions = db.relationship("Session", backref="workshop")
    code_id = db.Column('code_id', db.String(), db.ForeignKey('code.id'))
    #code:  Backref created a code on Workshop

class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.String(), primary_key=True)
    desc = db.Column(db.TEXT)
    workshops = db.relationship('Workshop', backref=db.backref('code', lazy=True))
    track_codes = db.relationship('TrackCode', backref=db.backref('code', lazy=True))

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

    def open(self):
        return(self.total_participants() < self.max_attendees)

    def is_past(self):
        if datetime.datetime.now() > self.date_time:
            return True
        else:
            return False

    def code(self):
        return self.workshop.code

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
    logs = db.relationship("EmailLog", backref="email_message", cascade="all, delete-orphan")

class EmailLog(db.Model):
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True)
    email_message_id = db.Column('email_message_id', db.Integer, db.ForeignKey('email_message.id'), primary_key=True)
    tracking_code = db.Column(db.String(), default=str(uuid.uuid4())[:16])
    opened = db.Column(db.Boolean, default=False)
    date_opened = db.Column(db.DateTime)

    def participant_name(self):
        return self.participant.display_name


# For marshalling objects to the database
# ----------------------------------------

class CodeDBSchema(ma.ModelSchema):
    class Meta:
        model = Code

class TrackCodeDBSchema(ma.ModelSchema):
    class Meta:
        model = TrackCode


class TrackDBSchema(ma.ModelSchema):
    class Meta:
        model = Track

class WorkshopDBSchema(ma.ModelSchema):
    class Meta:
        model = Workshop

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

class SearchSchema(ma.Schema):

    class FilterSchema(ma.Schema):
        field = fields.Str()
        value = fields.Str()

        @post_load
        def make_filter(self, data):
            return Filter(**data)

    query = fields.Str()
    date_restriction = fields.Str()
    filters = ma.List(ma.Nested(FilterSchema))
    total = fields.Integer(dump_only=True)
    hits = fields.List(fields.Dict(), dump_only=True)
    facets = fields.Dict(dump_only=True)
    ordered = True

    @post_load
    def make_search(self, data):
        return Search(**data)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid','givenName','email','surName','affiliation', 'displayName',
                  'eppn','title')
        ordered = True


class TrackAPISchema(ma.Schema):

    class TrackCodeSchema(ma.Schema):
        class Meta:
            fields = ('prereq','id', 'status', '_links')
        id = fields.Function(lambda obj: obj.code_id)
        status = fields.Method('get_status')
        _links = ma.Hyperlinks({
            'self': ma.URLFor('get_code', code='<code_id>'),
        })
        def get_status(self, obj):
            participant = g.user
            if participant == None:
                return "UNREGISTERED"
            for ps in participant.participant_sessions:
                if ps.session.code() != None and ps.session.code().id == obj.code.id:
                    if (ps.attended):
                        return "ATTENDED"
                    elif ps.session.is_past():
                        return "AWAITING_REVIEW"
                    else:
                        return "REGISTERED"
            return "UNREGISTERED"


    class Meta:
        # Fields to expose
        fields = ('id','title', 'description', '_links', 'codes')
        ordered = True

    codes = ma.List(ma.Nested(TrackCodeSchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_track', track_id='<id>'),
        'collection': ma.URLFor('get_tracks'),
        'image': ma.URLFor('get_track_image', track_id='<id>'),
    })
#    workshops = ma.Method('links_to_workshops')
#    def links_to_workshops(self, obj):
#        return list(map(lambda t: flask.url_for('get_workshop', id=t.workshop_id),
#                                                obj.track_workshops))


class ParticipantAPISchema(ma.Schema):

    class Meta:
        # Note that we don't surface the phone number or email address of any participants.
        fields = ('id', 'uid', 'display_name', 'bio', 'created', '_links')
        ordered = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'image': ma.URLFor('get_participant_image', id='<id>'),
        'workshops': ma.URLFor('user_workshops')
    })


class ParticipantSessionAPISchema(ma.Schema):
    class Meta:
        fields = ('participant', 'created', 'review_score', 'review_comment', 'attended', 'is_instructor')
        ordered = True
    participant = ma.Nested(ParticipantAPISchema)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'sessions': ma.URLFor('get_participant_sessions', id='<id>')
    })

class SessionAPISchema(ma.Schema):
    class Meta:
        fields = ('id', 'date_time', 'duration_minutes', 'instructor_notes',
                  '_links', 'max_attendees', 'participants', 'instructors','location',
                  'status')
        ordered = True
    participants = ma.List(ma.Nested(ParticipantSessionAPISchema))
    instructors = ma.List(ma.Nested(ParticipantAPISchema))
    status = fields.Method('get_status')

    def get_status(self, obj):
        participant = g.user
        if participant == None:
            return "UNREGISTERED"
        for ps in participant.participant_sessions:
            if ps.session.id == obj.id:
                if (ps.is_instructor):
                    return "INSTRUCTOR"
                if (ps.attended):
                    return "ATTENDED"
                elif ps.session.is_past():
                    return "AWAITING_REVIEW"
                else:
                    return "REGISTERED"
        return "UNREGISTERED"

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_session', id='<id>'),
        'collection': ma.URLFor('get_sessions'),
        'workshop': ma.URLFor('get_workshop', id='<workshop_id>'),
        'register': ma.URLFor('register', id='<id>'),
        'send_email': ma.URLFor('email_participants', id='<id>'),
        'messages': ma.URLFor('list_messages', id='<id>')
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


class CodeApiSchema(ma.Schema):
    class Meta:
        fields = ('id','desc','workshops')
        ordered = True
    workshops = ma.List(ma.Nested(WorkshopAPISchema))


class EmailMessageAPISchema(ma.Schema):

    class EmailLogAPISchema(ma.Schema):
        class Meta:
            fields = ('participant_id', 'opened', 'participant_name')
            ordered = True

    class Meta:
        fields = ('id', 'subject', 'content', 'sent_date', "author_id", 'logs')
        ordered = True
    logs = ma.List(ma.Nested(EmailLogAPISchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_messages', id='session_id'),
        'session': ma.URLFor('get_session', id='session_id')
    })



