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

class TrackWorkshop(db.Model):
    __tablename__ = 'track_workshop'
    track_id = db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True)
    workshop_id = db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'), primary_key=True)
    order = db.Column(db.Integer)


# user_session_table = db.Table('user_session', db.Base.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('session_id', db.Integer, db.ForeignKey('session.id'))
# )


# class User(db.Model):
#     id  = db.Column(db.Integer, primary_key=True)
#     display_name = db.Column(db.String())
#     image_file = db.Column(db.String())
#     sessions = db.relationship("Session", secondary=user_session_table, back_populates="attendees")
#     reviews = db.relationship("Review")


# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     score = db.Column(db.Integer)
#     comment = db.Column(db.TEXT())
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
#     session    = db.relationship('Session',
#                                backref=db.backref('review', lazy='dynamic'))
#     attendee_id = db.Column(db.Integer, db.ForeignKey('student.id'))
#     attendee    = db.relationship('User',
#                                backref=db.backref('review', lazy='dynamic'))



class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String())
    title = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    track_workshops = db.relationship('TrackWorkshop', backref='workshop')
#    sessions = db.relationship("Session", backref="workshop")

#class Session(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    date = db.Column(db.DateTime)
    #
    #     #instructor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #     #instructor = db.relationship("User", uselist=False, foreign_keys=[instructor_id])
    #
    #     # attendees = db.relationship("User", secondary=user_session_table, back_populates="sessions")
    #     # reviews = db.relationship("Review")
    #
#    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))


#
#     #todo: Link Workshop and Track
#     # sessions = #not sure
#     # tracks =  #notsure
#     # reviews =


class TrackDBSchema(ma.ModelSchema):
    class Meta:
        model = Track

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

class WorkshopDBSchema(ma.ModelSchema):
    class Meta:
        model = Workshop

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


class TrackWorkshopDBSchema(ma.ModelSchema):
    class Meta:
        model = TrackWorkshop

