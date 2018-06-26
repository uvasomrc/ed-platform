import datetime
import hashlib
import random
import uuid

import dateutil
import jwt
import icalendar
import pytz

from ed_platform import app, db, ma, RestException, discourse
from marshmallow import fields, post_load, post_dump
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
    participants = []
    workshops = []
    facets = []
    date_restriction = ""
    start = 0
    size = 0

    def __init__(self, query="", filters=[], date_restriction="",start=0, size=10):
        self.query = query
        self.filters = filters
        self.date_restriction = date_restriction
        self.start = start
        self.size = size

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
    def workshops(self):
        return self.code.workshops

class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    sub_title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    codes = db.relationship(lambda : TrackCode, order_by=TrackCode.order,  cascade="all, delete-orphan",
        backref=db.backref('track', lazy=True, single_parent=True))
    featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def workshops(self):
        workshops = []
        for code in self.codes:
            workshops = workshops + code.workshops()
        workshops = sorted(workshops, key=lambda w: w.next_session_date())
        return(workshops)


followers_table = db.Table('workshop_followers', db.metadata,
    db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id')),
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'))
)

class Workshop(db.Model):
    __tablename__ = 'workshop'

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    sessions = db.relationship("Session", backref="workshop", order_by="Session.date_time")
    instructor_id = db.Column('instructor_id', db.Integer, db.ForeignKey('participant.id'))
    code_id = db.Column('code_id', db.String(), db.ForeignKey('code.id'))
    discourse_enabled = db.Column(db.Boolean(), default=False)
    discourse_topic_id = db.Column(db.Integer, nullable=True)
    followers = db.relationship("Participant", secondary=followers_table, back_populates="following",  cascade="all, delete", single_parent=True)
    email_messages = db.relationship('EmailMessage', backref='workshop')

    #code:  Backref created a code on Workshop

    def discourse_url(self):
        if(self.discourse_topic_id):
            return discourse.urlForTopic(self.discourse_topic_id)

    def has_available_session(self):
        for s in self.sessions:
            if(s.is_open() and not s.is_full() and not s.is_past()): return True;
        return False

    @property
    def next_session(self):
        for s in self.sessions:
            if(not s.is_past()): return s;

    # Useful for sorting workshops, returns the maximum
    # possible date if there is no upcoming session.
    def next_session_date(self):
        for s in self.sessions:
            if(not s.is_past()): return s.date_time;
        return datetime.datetime(datetime.MAXYEAR,1,1)


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.String(), primary_key=True)
    description = db.Column(db.TEXT)
    workshops = db.relationship('Workshop', backref=db.backref('code', lazy=True))
    track_codes = db.relationship('TrackCode', backref=db.backref('code', lazy=True))

    def tracks(self):
        tracks = []
        for tc in self.track_codes :
            tracks.append(tc.track)
        return tracks

    def track_count(self):
        return len(self.tracks())


class Participant(db.Model):
    __tablename__ = 'participant'
    id  = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(), unique=True)
    display_name = db.Column(db.String())
    title = db.Column(db.String())
    email_address = db.Column(db.String())
    phone_number = db.Column(db.String())
    bio = db.Column(db.TEXT())
    image_file = db.Column(db.String())
    new_account = db.Column(db.Boolean(), default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_sessions = db.relationship('ParticipantSession', backref='participant')
    email_logs = db.relationship('EmailLog', backref='participant')
    sent_emails = db.relationship('EmailMessage', backref='author')
    use_gravatar = db.Column(db.Boolean(), default=True)
    role = db.Column(db.String(), default='USER')
    instructing_workshops = db.relationship('Workshop', backref=db.backref('instructor', lazy=True))
    following = db.relationship("Workshop", secondary=followers_table, back_populates="followers")

    def email_hash(self):
        h = hashlib.md5()
        h.update(self.email_address.strip().lower().encode('utf-8'))
        return h.hexdigest()

    def gravatar(self):
        return 'https://www.gravatar.com/avatar/%s?d=mm' % self.email_hash()

    def is_registered(self, session):
        return len([r for r in self.participant_sessions if r.session_id == session.id]) > 0

    def is_following(self, workshop):
        return len([w for w in self.following if w.id == workshop.id]) > 0

    def is_registered_for_workshop(self, workshop):
        for session in workshop.sessions:
            if(not(session.is_past()) and session.is_attendee(self)):
                return True
        return False

    def has_attended_workshop(self, workshop):
        for session in workshop.sessions:
            if(session.is_past() and session.is_attendee(self)):
                return True
        return False

    def register(self, session):
        if(self.is_registered(session)): return
        if(not session.is_open()):
           raise RestException(RestException.SESSION_WAIT)
        self.participant_sessions.append(ParticipantSession(
            participant_id = self.id, session_id=session.id
        ))


    def getWorkshops(self):
        workshops = []
        for ps in self.participant_sessions:
            workshops.append(ps.session.workshop)
        for ws in self.instructing_workshops:
            workshops.append(ws)
        workshops = list(filter(None, workshops))
        return workshops

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
    max_days_prior = db.Column(db.Integer) # Maximum number of days before the session starts that people can register.
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
    participant_sessions = db.relationship('ParticipantSession', backref='session')
    email_messages = db.relationship('EmailMessage', backref='session')

    def ical(self):
        """Returns an iCalendar, as a string that can be attached to an email message."""
        cal = icalendar.Calendar()
        cal.add('prodid', '-//%s//mxm.dk//' % app.config['NAME'])
        cal.add('version', app.config['VERSION'])

        event = icalendar.Event()
        event.add('summary', self.workshop.title)
        event.add('description', self.workshop.description)
        event.add('location', self.location)
        event.add('dtstart', pytz.utc.localize(self.date_time))
        event.add('dtend', pytz.utc.localize(self.end_date_time()))
        event.add('dtstamp', pytz.utc.localize(datetime.datetime.now()))
        event.add('uid', str("CADRE-ACADEMY-SESSION-%i" % self.id))
        cal.add_component(event)
        return cal.to_ical()

    def total_participants(self):
        return len(self.participant_sessions)

    def end_date_time(self):
        return (self.date_time + datetime.timedelta(minutes=self.duration_minutes))

    def start_date_time_local(self):
        dt_aware = pytz.utc.localize(self.date_time)
        dt_local = dt_aware.astimezone(pytz.timezone(app.config.get('TIMEZONE')))
        return dt_local

    def end_date_time_local(self):
        dt_aware = pytz.utc.localize(self.end_date_time())
        dt_local = dt_aware.astimezone(pytz.timezone(app.config.get('TIMEZONE')))
        return dt_local

    def date_open(self):
        if(self.max_days_prior == None or self.max_days_prior <= 0): return None;
        else : return(self.date_time - datetime.timedelta(days = self.max_days_prior));

    def is_full(self):
        return(self.total_participants() >= self.max_attendees)

    def is_open(self):
        if(self.max_days_prior == None or self.max_days_prior <= 0): return True;
        else : return(self.date_open() <= datetime.datetime.now());

    def is_past(self):
        if datetime.datetime.now() > self.date_time:
            return True
        else:
            return False

    def is_attendee(self, participant):
        for ps in self.participant_sessions:
            if(ps.participant == participant):
                return True
        return False

    def confirmation_sent(self):
        for email in self.email_messages:
            if(email.is_confirmation()): return True
        return False

    def followers_notified_seats(self):
        for email in self.email_messages:
            if(email.is_notify_followers_seats()): return True
        return False

    def followers_notified_session(self):
        for email in self.email_messages:
            if(email.is_notify_followers_session()): return True
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
    confirmed = db.Column(db.Boolean, default=False)
    attended = db.Column(db.Boolean, default=False)

class EmailMessage(db.Model):
    __tablename__ = 'email_message'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    session_id = db.Column('session_id', db.Integer, db.ForeignKey('session.id'))
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
    subject = db.Column(db.String())
    content = db.Column(db.TEXT())
    sent_date = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column('author_id', db.Integer, db.ForeignKey('participant.id'))
    logs = db.relationship("EmailLog", backref="email_message", cascade="all, delete-orphan")

    TYPE_FOLLOWERS = "Instructor to Followers"
    TYPE_ATTENDEES = "Instructor to Attendees"
    TYPE_CONFIRM = "Upcoming Workshop Reminder"
    TYPE_NOTIFY_FOLLOWERS_SEATS = "Upcoming Workshop Available"
    TYPE_NOTIFY_FOLLOWERS_SESSION = "New Session Notification"

    def is_confirmation(self):
        return self.type == self.TYPE_CONFIRM

    def is_notify_followers_seats(self):
        return self.type == self.TYPE_NOTIFY_FOLLOWERS_SEATS

    def is_notify_followers_session(self):
        return self.type == self.TYPE_NOTIFY_FOLLOWERS_SESSION


class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    date_sent = db.Column(db.DateTime, default=datetime.datetime.now)
    tracking_code = db.Column(db.String(), default=str(uuid.uuid4())[:16])
    opened = db.Column(db.Boolean, default=False)
    date_opened = db.Column(db.DateTime)
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), nullable=False)
    email_message_id = db.Column('email_message_id', db.Integer, db.ForeignKey('email_message.id'))
    session_id = db.Column('session_id', db.Integer, db.ForeignKey('session.id'))
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
    error = db.Column(db.TEXT())

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
    start = fields.Integer()
    size = fields.Integer()
    date_restriction = fields.Str()
    filters = ma.List(ma.Nested(FilterSchema))
    total = fields.Integer(dump_only=True)
    workshops = fields.List(fields.Dict(), dump_only=True)
    participants = fields.List(fields.Dict(), dump_only=True)
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


class ParticipantAPISchema(ma.Schema):

    class Meta:
        # Note that we don't surface the phone number or email address of any participants.
        fields = ('id', 'uid','display_name', 'title',  'bio', 'created', 'new_account',
                 'gravatar', 'use_gravatar', 'role', '_links', 'email_address', 'image_file')
        ordered = True
        dateformat = "iso"

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_participant', id='<id>'),
        'collection': ma.URLFor('get_participants'),
        'workshops': ma.URLFor('user_workshops')
    })

    @post_dump
    def postprocess(self, data):
        """Move the image url into the link."""
        data['_links']['image'] = data['image_file']
        del data['image_file']




class ParticipantSessionAPISchema(ma.Schema):
    class Meta:
        fields = ('participant', 'created', 'review_score', 'review_comment', 'attended', 'confirmed')
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
                  '_links', 'max_attendees', 'participant_sessions', 'location',
                  'status', 'total_participants', 'max_days_prior', 'date_open')
        ordered = True
    participant_sessions = ma.List(ma.Nested(ParticipantSessionAPISchema))
    status = fields.Method('get_status')
    dateformat = "iso"

    def get_status(self, obj):
        participant = g.user
        if participant is None or participant.role == "ANON":
            return "NO_USER"
        if (obj.workshop in participant.instructing_workshops):
            return "INSTRUCTOR"
        for ps in participant.participant_sessions:
            if ps.session.id == obj.id:
                if (ps.attended):
                    return "ATTENDED"
                elif ps.session.is_past():
                    return "AWAITING_REVIEW"
                else:
                    return "REGISTERED"
        if not obj.is_open():
            return "NOT_YET_OPEN"
        if obj.is_full():
            return "FULL"
        else:
            return "UNREGISTERED"

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_session', id='<id>'),
        'collection': ma.URLFor('get_sessions'),
        'workshop': ma.URLFor('get_workshop', id='<workshop_id>'),
        'register': ma.URLFor('register', id='<id>'),
        'email': ma.URLFor('email_participants', id='<id>'),
    })


class WorkshopAPISchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', '_links', 'sessions','code_id', 'instructor',
                  'discourse_enabled', 'discourse_url', 'discourse_topic_id', 'status', 'followers',
                  'next_session')
        ordered = True
    instructor = ma.Nested(ParticipantAPISchema)
    sessions = ma.List(ma.Nested(SessionAPISchema))
    followers = ma.List(ma.Nested(ParticipantAPISchema))
    next_session = ma.Nested(SessionAPISchema)

    status = fields.Method('get_status')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_workshop', id='<id>'),
        'collection': ma.URLFor('get_workshops'),
        'posts': ma.URLFor('get_discourse_topic', id='<id>'),
        'image': ma.URLFor('get_workshop_image', id='<id>'),
        'tracks': ma.URLFor('get_workshop_tracks', id='<id>'),
        'sessions': ma.URLFor('get_workshop_sessions', id='<id>'),
        'follow': ma.URLFor('follow_workshop', id='<id>'),
        'email': ma.URLFor('email_followers', id='<id>')
    })

    def get_status(self, obj):
        participant = g.user
        if participant is None or participant.role == "ANON":
            return "NO_USER"
        elif (obj.instructor.uid == participant.uid):
            return "INSTRUCTOR"
        elif (obj in participant.following):
            return "FOLLOWING"
        elif (participant.has_attended_workshop(obj)):
            return "ATTENDED"
        elif (participant.is_registered_for_workshop(obj)):
            return "REGISTERED"
        elif (obj.has_available_session()):
            return "UNREGISTERED"
        else:
            return "UNAVAILABLE"

class CodeApiSchema(ma.Schema):

    class Meta:
        fields = ('id', 'description', 'workshops', 'track_count', "_links")
        ordered = True
    workshops = fields.Method('sort_workshops_dumped')

    def sort_workshops_dumped(self, obj):
        workshops = sorted(obj.workshops, key=lambda w: w.next_session_date())
        return WorkshopAPISchema().dump(workshops, many=True)[0]

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_code', code='<id>'),
    })

class TrackAPISchema(ma.Schema):

    class TrackCodeSchema(ma.Schema):
        class Meta:
            fields = ('prereq','id', 'status', '_links')
            dateformat = "iso"
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
        fields = ('id','title', 'sub_title', 'description', '_links', 'codes', 'image_file', 'featured')
        ordered = True

    codes = ma.List(ma.Nested(TrackCodeSchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_track', track_id='<id>'),
        'collection': ma.URLFor('get_tracks'),
    })

    @post_dump
    def postprocess(self, data):
        """Move the image url into the link."""
        data['_links']['image'] = data['image_file']
        del data['image_file']

class TrackWithWorkshopsByWeekSchema(ma.Schema):
    class Meta:
        fields = ('id','title', 'sub_title', 'description', '_links', 'workshops')
        ordered = True
    workshops = fields.Method('group_workshops_by_date')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_track', track_id='<id>'),
        'collection': ma.URLFor('get_tracks'),
        'image': ma.URLFor('get_track_image', track_id='<id>'),
    })

    def group_workshops_by_date(self, obj):
        workshops = WorkshopAPISchema().dump(obj.workshops(), many=True)[0]
        return workshops

class EmailMessageAPISchema(ma.Schema):

    class EmailLogAPISchema(ma.Schema):
        class Meta:
            fields = ('participant_id', 'opened', 'participant_name')
            ordered = True

    class Meta:
        fields = ('id', 'subject', 'content', 'sent_date', "author_id", 'logs')
        ordered = True
        dateformat = "iso"

    logs = ma.List(ma.Nested(EmailLogAPISchema))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_messages', id='session_id'),
        'session': ma.URLFor('get_session', id='session_id')
    })



