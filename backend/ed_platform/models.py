import flask
from ed_platform import app, db, ma



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
    display_name = db.Column(db.String())
    email_address = db.Column(db.String())
    phone_number = db.Column(db.String())
    bio = db.Column(db.TEXT())
    image_file = db.Column(db.String())
    created = db.Column(db.DateTime)
    participant_sessions = db.relationship('ParticipantSession', backref='participant')

class Session(db.Model):
    """A Workshop Session or Class, but Session / Class are too common and we get conflicts as we lack a namespace, and wanted a single term. """
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    instructor_notes = db.Column(db.TEXT())
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
    participant_sessions = db.relationship('ParticipantSession', backref='session')

class ParticipantSession(db.Model):
    __tablename__ = 'participant_session'
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True)
    session_id = db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True)
    created  = db.Column(db.DateTime)
    review_score = db.Column(db.Integer)
    review_comment = db.Column(db.TEXT())
    attended = db.Column(db.Boolean)
    is_instructor = db.Column(db.Boolean)


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



# For marshalling objects to the Front End
# ----------------------------------------

class TrackAPISchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','title', 'description', '_links')
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

class WorkshopAPISchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', '_links')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_workshop', id='<id>'),
        'collection': ma.URLFor('get_workshops'),
        'image': ma.URLFor('get_workshop_image', id='<id>'),
        'tracks': ma.URLFor('get_workshop_tracks', id='<id>'),
        #todo: Add links to tracks and sessions.
    })
#    track_workshops = ma.List(ma.HyperlinkRelated('get_track', id='<track_id>'))
