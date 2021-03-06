import datetime
from collections import OrderedDict

import elasticsearch
import magic
import os
from flask import jsonify, request, send_file, session, redirect, g, render_template, json, Response
from sqlalchemy import desc

from ed_platform import app, db, models, sso, RestException, elastic_index, profile_photos, discourse, notify, \
    file_server
from flask_httpauth import HTTPTokenAuth
from dateutil import parser
from operator import itemgetter,and_
from ed_platform.wrappers import requires_roles

user_schema = models.UserSchema()
track_schema = models.TrackAPISchema()
workshop_schema = models.WorkshopAPISchema()
session_schema = models.SessionAPISchema()
participant_schema = models.ParticipantAPISchema()
email_schema = models.EmailMessageAPISchema()

track_db_schema = models.TrackDBSchema()
workshop_db_schema = models.WorkshopDBSchema()
session_db_schema = models.SessionDBSchema()
participant_db_schema = models.ParticipantDBSchema()
participant_session_db_schema = models.ParticipantSessionDBSchema()
email_message_db_schema = models.EmailMessageDbSchema()


auth = HTTPTokenAuth('Bearer')
'''Many endpoints will take the current user into account when returning values. 
   Since the flask_htttauth will throw an error if the authentication fails, we
   return a default participant with a role of ANON - and must then check the
   roles of the user if the endpoint is restricted to logged-in users.'''
defaultParticipant = models.Participant()
defaultParticipant.id = 0
defaultParticipant.role = "ANON"


@auth.verify_token
def verify_token(token):
    try:
        resp = models.Participant.decode_auth_token(token)
        g.user = models.Participant.query.filter_by(uid=resp).first()
    except:
        g.user = defaultParticipant

    if(g.user != None):
        return True
    else:
        g.user = defaultParticipant
        return True

@app.route('/api', methods=['GET'])
def root():
    return "ED Platform API"


# User Accounts
# *****************************
@sso.login_handler
def login(user_info):
    if (app.config["DEVELOPMENT"]) :
        uid = app.config["SSO_DEVELOPMENT_UID"]
    else :
        uid = user_info['uid']

    participant = models.Participant.query.filter_by(uid=uid).first()
    if(participant is None) :
        participant = models.Participant(uid=uid,
                                         display_name=user_info["givenName"],
                                         email_address=user_info["email"])
        if("Surname" in user_info):
            participant.display_name = participant.display_name + " " + user_info["Surname"]

        if("displayName" in user_info and len(user_info["displayName"]) > 1):
            participant.display_name = user_info["displayName"]

        db.session.add(participant)
        db.session.commit()
    # redirect users back to the front end, include the new auth token.
    auth_token = participant.encode_auth_token().decode()
    response_url = ("%s/%s" % (app.config["FRONTEND_AUTH_CALLBACK"], auth_token))
    return redirect(response_url)

@app.route('/api/backdoor/<string:user>/<string:code>')
def backdoor(user, code):
    '''A backdoor that allows someone to log in as a default user, if they
       are in a staging environment. Added so our designer, who doesn't have a
       shibboleth account, can still see the system.'''
    if (app.config["STAGING"] and code == app.config["BACKDOOR_CODE"]) :
        participant = models.Participant.query.filter_by(uid=user).first()
        auth_token = participant.encode_auth_token().decode()
        response_url = ("%s/%s" % (app.config["FRONTEND_AUTH_CALLBACK"], auth_token))
        return redirect(response_url)
    else :
        raise RestException(RestException.NOT_FOUND)


@app.route('/api/user')
@auth.login_required
@requires_roles('USER','ADMIN')
def status():
    return jsonify(participant_schema.dump(g.user).data)

@app.route('/api/logout')
@auth.login_required
def logout():
    #fixme: Logout should invalidate the auth token.
    session.pop('user')
    return redirect('/api/')

@app.route('/api/user/workshops', methods=["GET"])
@auth.login_required
@requires_roles('USER','ADMIN')
def user_workshops():
    for w in g.user.getWorkshops():
        print("Workshop: " + str(w))
    return models.WorkshopAPISchema().jsonify(g.user.getWorkshops(),many=True)

@app.route('/api/user/following', methods=['GET'])
@auth.login_required
@requires_roles('USER','ADMIN')
def following():
    return models.WorkshopAPISchema().jsonify(g.user.following,many=True)

# Participants Admin
# *****************************
@app.route('/api/participant', methods=['GET'])
@auth.login_required
@requires_roles('ADMIN')
def list_participants():
    all_participants = models.Participant.query.order_by('email_address').all()
    return models.ParticipantAPISchema().jsonify(all_participants, many=True)

@app.route('/api/participant/emails.csv', methods=['GET'])
@auth.login_required
@requires_roles('ADMIN')
def list_participant_emails():
    email_results = db.session.query(models.Participant.email_address).order_by('email_address').all()
    all_emails = [r for (r, ) in email_results]
    return Response(",".join(filter(None,all_emails)), mimetype='text/csv')

# Codes
# *****************************
@app.route('/api/code', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def create_code():
    request_data = request.get_json()
    new_code = models.CodeDBSchema().load(request_data).data
    db.session.add(new_code)
    db.session.commit()
    return models.CodeDBSchema().jsonify(new_code)

@app.route('/api/code', methods=['GET'])
@auth.login_required
def get_codes():
    codes = list(map(lambda c: models.CodeApiSchema().dump(c).data, models.Code.query.order_by(models.Code.id).all()))
    return jsonify(codes)

@app.route('/api/code/<string:code>')
@auth.login_required
def get_code(code):
    code = models.Code.query.filter_by(id=code).first()
    if (code == None):
        raise RestException(RestException.NO_SUCH_CODE)
    else:
        return models.CodeApiSchema().jsonify(code)

# Tracks
# *****************************

def set_track_codes(track, codes_as_json):
    track_codes = []
    order = 0
    for code in codes_as_json:
        db_code = models.Code.query.filter_by(id=code['id']).first()
        if(db_code == None):
            raise RestException(RestException.NO_SUCH_CODE)
        track_codes.append(models.TrackCode(track_id=track.id, code_id=code["id"],
                                             prereq=code["prereq"], order=order))
        order += 1
    track.codes = track_codes
    return track

@app.route('/api/track', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def create_track():
    request_data = request.get_json()
    codes_as_json = request_data["codes"]
    request_data["codes"] = []
    new_track = track_db_schema.load(request_data).data
    set_track_codes(new_track, codes_as_json)
    db.session.add(new_track)
    db.session.commit()
    return track_schema.jsonify(new_track)

@app.route('/api/track/<int:id>', methods=['PUT'])
@auth.login_required
@requires_roles('ADMIN')
def update_track(id):
    request_data = request.get_json()
    codes_as_json = request_data["codes"]
    request_data['id'] = id
    request_data["codes"] = []
    new_track = track_db_schema.load(request_data).data
    set_track_codes(new_track, codes_as_json)
    db.session.add(new_track)
    db.session.commit()
    return track_schema.jsonify(new_track)


def update_tracks_for_participant(track, participant):
    for code in track:
        code.status = participant.get_status_for_code(code)

@app.route('/api/track', methods=['GET'])
@auth.login_required
def get_tracks():
    tracks = list(map(lambda t: track_schema.dump(t).data, models.Track.query.all()))
    return jsonify({"tracks": tracks})

@app.route('/api/track/featured', methods=['GET'])
@auth.login_required
def get_featured_tracks():
    tracks = list(map(lambda t: track_schema.dump(t).data, models.Track.query.filter_by(featured=True).all()))
    return jsonify({"tracks": tracks})

@app.route('/api/track/<int:track_id>')
@auth.login_required
def get_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if(track is None):
        return jsonify(error=404, text=str("no such track.")), 404
    return track_schema.jsonify(track)

@app.route('/api/track/<int:track_id>/workshops')
@auth.login_required
def track_workshops(track_id):
    ''' Returns a list of workshops for a given track, grouped by week'''
    order = request.args.get('order')

    track = models.Track.query.filter_by(id=track_id).first()

    workshops = []
    for code in track.codes:
        workshops = workshops + code.workshops()
    workshops = sorted(workshops, key=lambda w: w.next_session_date())

    by_date = OrderedDict()
    for w in workshops:
        if (w.next_session is not None):
            index = w.next_session.date_time - datetime.timedelta(days=w.next_session.date_time.weekday())
            index = index.strftime('%Y-%m-%d')
        else:
            index = ""
        if (index not in by_date): by_date[index] = []
        by_date[index].append(models.WorkshopAPISchema().dump(w).data)

    date_array = []
    for (date, workshops) in by_date.items():
        date_array.append( { "id": date, "workshops": workshops })

    return jsonify(date_array)

@app.route('/api/track/<int:track_id>', methods=['DELETE'])
@auth.login_required
@requires_roles('ADMIN')
def remove_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if(track is None):
        return jsonify(error=404, text=str("no such track.")), 404

    db.session.delete(track)
    db.session.commit()
    return ""

@app.route('/api/track/<int:id>/codes', methods=['PATCH'])
@auth.login_required
@requires_roles('ADMIN')
def update_track_codes(id):
    request_data = request.get_json()
    # Clear existing track codes.
#    models.TrackCode.query.filter_by(track_id = id).delete()
    track = models.Track.query.filter_by(id=id).first()
    set_track_codes(track, request_data)
    db.session.add(track)
    db.session.commit()
    return jsonify(track_schema.dump(track))

@app.route('/api/track/<int:id>/image', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def set_track_image(id):
    file = request.files.get('image')
    extension = file.filename.rsplit('.', 1)[1].lower()
    track = models.Track.query.filter_by(id=id).first()
    filename = file_server.save_track_image(file, track, extension, file.content_type)
    track.image_file = filename
    db.session.add(track)
    db.session.commit()
    return filename

# Workshop
# *****************************


@app.route('/api/workshop')
@auth.login_required
def get_workshops():
    workshops = list(map(lambda t: workshop_schema.dump(t).data,
                         models.Workshop.query.all()))
    return jsonify({"workshops": workshops})

@app.route('/api/workshop/search', methods=['POST'])
@auth.login_required
def search_workshops():
    request_data = request.get_json()
    search = models.SearchSchema().load(request_data).data
    try:
        results = elastic_index.search_workshops(search)
    except elasticsearch.ElasticsearchException as e:
        raise RestException(RestException.ELASTIC_ERROR)
    search.total = results.hits.total
    facets = {}
    for facet_name in results.facets:
        counts = []
        for category, hit_count, is_selected in results.facets[facet_name]:
            counts.append({'category':category, 'hit_count':hit_count, 'is_selected': is_selected})
        facets[facet_name] = counts
    print(jsonify(facets))
    search.facets = facets
    workshops = []
    for hit in results:
        workshop = models.Workshop.query.filter_by(id=hit.id).first()
        if(workshop is not None):
            workshops.append(workshop)
    search.workshops = workshop_schema.dump(workshops, many=True).data
    return models.SearchSchema().jsonify(search)

@app.route('/api/workshop', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def create_workshop():
    request_data = request.get_json()
    db_code = None
    if('code_id' in request_data and
               request_data['code_id'] is not None and
               request_data['code_id'] != ''):
        db_code = models.Code.query.filter_by(id=request_data['code_id']).first()
        if (db_code == None): raise RestException(RestException.NO_SUCH_CODE)

    new_sessions = []
    if('sessions' in request_data):
        for session in request_data['sessions']:
            if('id' in session and session['id'] > 0):
                new_session = models.Session.query.filter_by(id=session['id']).first()
            else :
                new_session = models.Session()
            fields = ['date_time', 'duration_minutes', 'location', 'instructor_notes', 'max_attendees', 'max_days_prior']
            for field in fields:
                if(field in session):
                    setattr(new_session, field, session[field])
            new_sessions.append(new_session)

    request_data['sessions'] = []
    new_workshop = workshop_db_schema.load(request_data).data
    if(db_code):
        new_workshop.code = db_code
    else:
        new_workshop.code = None
    new_workshop.sessions = new_sessions

    db.session.add(new_workshop)
    db.session.commit()
    elastic_index.add_workshop(new_workshop)

    if("discourse_enabled" in request_data and
           request_data["discourse_enabled"] and
           new_workshop.discourse_topic_id is None):
        topic = discourse.createTopic(new_workshop)
        new_workshop.discourse_topic_id = topic.id
        db.session.add(new_workshop)
        db.session.commit()


    return workshop_schema.jsonify(new_workshop)

@app.route('/api/workshop/featured')
def get_featured_workshops():
    # returns a list of 6 workshops, prefering upcoming workshops, but always returning something.
    workshops = (models.Workshop.query.
                outerjoin(models.Session, and_(models.Workshop.id == models.Session.workshop_id,
                    models.Session.date_time >= datetime.datetime.now())).
                order_by(models.Session.date_time).
                limit(6)
                )
    return models.WorkshopAPISchema().jsonify(workshops, many=True)


@app.route('/api/workshop/upcoming')
def get_upcoming_workshops():
    # returns a list of all upcoming workshops, ordered by date
    workshops = (models.Workshop.query.
                join(models.Session, and_(models.Workshop.id == models.Session.workshop_id,
                    models.Session.date_time >= datetime.datetime.now())).
                order_by(models.Session.date_time)
                )
    return models.WorkshopAPISchema().jsonify(workshops, many=True)

@app.route('/api/workshop/<int:id>/discourse', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def add_discourse_topic(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop.discourse_topic_id is None):
        topic = discourse.createTopic(workshop)
        workshop.discourse_topic_id = topic.id

    workshop.discourse_enabled = True
    db.session.add(workshop)
    db.session.commit()
    return (jsonify(workshop_schema.dump(workshop)))

@app.route('/api/workshop/<int:id>/discourse', methods=['GET'])
@auth.login_required
def get_discourse_topic(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop.discourse_topic_id is None): raise RestException(RestException.NO_DISCOURSE_TOPIC)
    topic = discourse.getTopic(workshop)
    if(topic is None): raise RestException(RestException.NO_DISCOURSE_TOPIC)

    for post in topic.posts:
        participant = models.Participant.query.filter_by(uid=post.uid).first()
        if(participant is not None):
            post.participant = models.ParticipantAPISchema().dump(participant).data
    json = topic.toJSON()
    return(json)

@app.route('/api/workshop/<int:id>/discourse/post', methods=['POST'])
@auth.login_required
@requires_roles('USER','ADMIN')
def add_discourse_post(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    message = request.get_json()["raw"]
    discourse.createPost(workshop, g.user, message)
    topic = discourse.getTopic(workshop)
    return(topic.toJSON())


@app.route('/api/workshop/<int:id>/instructor/<int:instructor_id>', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def set_instructor(id, instructor_id):
    participant = models.Participant.query.filter_by(id=id).first()
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(participant is None):
        raise RestException(RestException.NO_SUCH_PARTICIPANT)
    if(workshop is None):
        raise RestException(RestException.NO_SUCH_WORKSHOP)
    workshop.instructor = participant
    db.session.add(workshop)
    db.session.commit()
    return (jsonify(workshop_schema.dump(workshop)))


@app.route('/api/workshop/<int:id>')
@auth.login_required
def get_workshop(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop is None):
        return jsonify(error=404, text=str("no such workshop.")), 404
    return workshop_schema.jsonify(workshop)


@app.route('/api/workshop/<int:id>', methods=['DELETE'])
@auth.login_required
@requires_roles('ADMIN')
def remove_workshop(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop is None): return ""
    if(len(workshop.sessions) > 0):
        return jsonify(error=409, text=str("This workshop has existing sessions. Please remove the sessionfeas first.")), 409
    db.session.delete(workshop)
    db.session.commit()
    elastic_index.remove_workshop(id)
    return ""

@app.route('/api/workshop/<int:id>/tracks')
@auth.login_required
def get_workshop_tracks(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    tracks = []
    if(workshop.code != None):
        tracks = workshop.code.tracks()
    return models.TrackAPISchema().jsonify(tracks, many=True)

@app.route('/api/workshop/<int:id>/sessions', methods=['GET'])
@auth.login_required
def get_workshop_sessions(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    sessions = list(map(lambda s: session_schema.dump(s).data, workshop.sessions))
    return jsonify({"sessions": sessions})

@app.route('/api/workshop/<int:id>/image')
def get_workshop_image(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    return send_file("static/" + workshop.image_file, mimetype='image/png')

@app.route('/api/workshop/<int:id>/follow', methods=['POST'])
@auth.login_required
@requires_roles('USER','ADMIN')
def follow_workshop(id):
    participant = g.user
    workshop = models.Workshop.query.filter_by(id=id).first()
    workshop.followers.append(participant)
    db.session.add(workshop)
    db.session.commit()
    return workshop_schema.jsonify(workshop)

@app.route('/api/workshop/<int:id>/follow', methods=['DELETE'])
@auth.login_required
@requires_roles('USER','ADMIN')
def unfollow_workshop(id):
    participant = g.user
    workshop = models.Workshop.query.filter_by(id=id).first()
    workshop.followers.remove(participant)
    db.session.commit()
    return workshop_schema.jsonify(workshop)

@app.route('/api/workshop/<int:id>/follow/<string:tracking_code>', methods=['DELETE'])
@auth.login_required
def unfollow_workshop_using_token(id, tracking_code):
    """Unfollow the workshop using a token, without logging in."""
    log = models.EmailLog.query.filter_by(tracking_code=tracking_code, workshop_id=id).first()
    if(log is None):
        raise RestException(RestException.INVALID_TRACKING_CODE)
    participant = log.participant
    workshop = models.Workshop.query.filter_by(id=id).first()
    workshop.followers.remove(participant)
    db.session.commit()
    return workshop_schema.jsonify(workshop)

@app.route('/api/workshop/<int:id>/email', methods=['POST'])
@auth.login_required
def email_followers(id):
    instructor = g.user
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(g.user.role != 'ADMIN' and instructor != workshop.instructor):
        raise RestException(RestException.NOT_INSTRUCTOR)

    request_data = request.get_json()
    email = email_message_db_schema.load(request_data).data
    email.type = models.EmailMessage.TYPE_FOLLOWERS
    email.author = instructor
    email.workshop = workshop
    for participant in workshop.followers:
         email_log = models.EmailLog(participant=participant, email_message=email)
         email.logs.append(email_log)

         notify.message_to_followers(instructor=instructor, subject=email.subject,
                                     content=email.content,
                                     participant=participant, workshop=workshop)
    db.session.add(email)
    db.session.commit()

    return email_schema.jsonify(email)

@app.route('/api/workshop/<int:id>/email', methods=['GET'])
@auth.login_required
def follow_emails(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    return (email_schema.jsonify(workshop.email_messages, many=True))

# Sessions
# *****************************

@app.route('/api/session', methods=['GET'])
@auth.login_required
def get_sessions():
    sessions = list(map(lambda t: session_schema.dump(t).data,
                         models.Session.query.all()))
    return jsonify({"sessions": sessions})


@app.route('/api/session', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def create_session():
    request_data = request.get_json()
    new_session = session_db_schema.load(request_data).data
    db.session.add(new_session)
    db.session.commit()
    return session_schema.jsonify(new_session)

@app.route('/api/session/<int:id>', methods=['GET'])
@auth.login_required
def get_session(id):
    session = models.Session.query.filter_by(id=id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    return  session_schema.jsonify(session)

@app.route('/api/session/<int:id>', methods=['DELETE'])
@auth.login_required
@requires_roles('ADMIN')
def remove_session(id):
    session = models.Session.query.filter_by(id=id).first()
    db.session.delete(session)
    db.session.commit()
    return ""

@app.route('/api/session/<int:id>/register', methods=['GET'])
@auth.login_required
def view_registration(id):
    participant = g.user
    session = models.Session.query.filter_by(id=id).first()
    return (jsonify(participant_session_db_schema.dump(participant.getParticipantSession(session)).data))

@app.route('/api/session/<int:id>/register', methods=['POST'])
@auth.login_required
@requires_roles('USER','ADMIN')
def register(id):
    participant = g.user
    session = models.Session.query.filter_by(id=id).first()
    if(session is None):
        raise RestException(RestException.NO_SUCH_SESSION, 404)
    if(session.max_attendees <= len(session.participant_sessions)):
        raise RestException(RestException.SESSION_FULL, 404)
    else:
        participant.register(session)
        tracking_code = notify.registered(participant, session)
        email_log = models.EmailLog(participant=participant,
                                session_id=session.id,
                                type="REGISTER", tracking_code=tracking_code)
        db.session.add(email_log)

    if(participant in session.workshop.followers):
        session.workshop.followers.remove(participant) # Don't follow a workshop you are now registered for.
        db.session.merge(participant)
    db.session.commit()
    return models.SessionAPISchema().jsonify(session)

@app.route('/api/session/<int:id>/register', methods=['PUT'])
@auth.login_required
@requires_roles('USER','ADMIN')
def review(id):

    participant = g.user
    reg = models.ParticipantSession.query.filter_by(participant_id=participant.id,
                                                    session_id=id).first()
    updates = request.get_json()
    reg.review_score = updates["review_score"]
    reg.review_comment = updates["review_comment"]
    reg.attended = True

    db.session.commit()
    return (jsonify(participant_session_db_schema.dump(reg).data))


@app.route('/api/session/<int:id>/register', methods=['DELETE'])
@auth.login_required
@requires_roles('USER','ADMIN')
def unregister(id):
    participant = g.user
    participant = models.Participant.query.filter_by(id=participant.id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    session = models.Session.query.filter_by(id=id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    participant_session = participant.getParticipantSession(session)
    if(participant_session is not None):
        db.session.delete(participant_session)
        db.session.commit()
    session = models.Session.query.filter_by(id=id).first()
    return models.SessionAPISchema().jsonify(session)

@app.route('/api/session/<int:id>/confirm/<string:tracking_code>', methods=['POST'])
@auth.login_required
# @requires_roles('USER','ADMIN')  Anyone can post to this, since it contains a token.
def confirm_attending(id, tracking_code):
    # locate email message in logs by the token/tracking code
    log = models.EmailLog.query.filter_by(tracking_code=tracking_code, session_id=id).first()
    if(log is None):
        raise RestException(RestException.INVALID_TRACKING_CODE)
    participant = log.participant
    session = models.Session.query.filter_by(id=id).first()
    participant_session = participant.getParticipantSession(session)
    participant_session.confirmed = True
    db.session.add(participant_session)
    db.session.commit()
    return models.SessionAPISchema().jsonify(session)

@app.route('/api/session/<int:id>/confirm/<string:tracking_code>', methods=['DELETE'])
@auth.login_required
# @requires_roles('USER','ADMIN')  Anyone can post to this, since it contains a token.
def confirm_not_attending(id, tracking_code):
    # locate email message in logs by the token/tracking code
    log = models.EmailLog.query.filter_by(tracking_code=tracking_code, session_id=id).first()
    if(log is None):
        raise RestException(RestException.INVALID_TRACKING_CODE)
    participant = log.participant
    session = models.Session.query.filter_by(id=id).first()
    participant_session = participant.getParticipantSession(session)
    db.session.delete(participant_session)
    db.session.commit()
    return models.SessionAPISchema().jsonify(session)

@app.route('/api/session/<int:id>/email', methods=['POST'])
@auth.login_required
def email_participants(id):
    instructor = g.user
    session = models.Session.query.filter_by(id=id).first()
    if(g.user.role != 'ADMIN' and instructor != session.workshop.instructor):
        raise RestException(RestException.NOT_INSTRUCTOR)

    request_data = request.get_json()
    email = email_message_db_schema.load(request_data).data
    email.type = models.EmailMessage.TYPE_ATTENDEES
    email.author = instructor
    email.session = session
    for ps in session.participant_sessions:
        email_log = models.EmailLog(participant=ps.participant,
                                    email_message=email)
        email.logs.append(email_log)
        notify.message_to_attendees(instructor=instructor,
                                    subject=email.subject,
                                    content=email.content,
                                    participant=ps.participant,
                                    session=session)

    db.session.add(email)
    db.session.commit()

    return email_schema.jsonify(email)

@app.route('/api/session/<int:id>/email', methods=['GET'])
@auth.login_required
def list_messages(id):
    session = models.Session.query.filter_by(id=id).first()
    return (email_schema.jsonify(session.email_messages, many=True))

# Participants
# *****************************

@app.route('/api/participant', methods=['GET'])
@auth.login_required
def get_participants():
    participants = list(map(lambda t: participant_schema.dump(t).data,
                         models.Participant.query.all()))
    return jsonify({"participants": participants})

@app.route('/api/participant', methods=['POST'])
@auth.login_required
@requires_roles('ADMIN')
def create_participant():
    request_data = request.get_json()
    participant = participant_db_schema.load(request_data).data
    db.session.add(participant)
    db.session.commit()
    return participant_schema.jsonify(participant)

@app.route('/api/participant/<int:id>', methods=['PUT'])
@auth.login_required
def update_participant(id):
    request_data = request.get_json()
    participant = models.Participant.query.filter_by(id=id).first()

    if(g.user.id != id):
        raise RestException(RestException.NOT_YOUR_ACCOUNT, 403)

    participant.display_name = request_data['display_name']
    participant.new_account = False;
    participant.bio = request_data['bio']
    participant.use_gravatar = request_data['use_gravatar']

    db.session.add(participant)
    db.session.commit()
    return participant_schema.jsonify(participant)


@app.route('/api/participant/<int:id>', methods=['GET'])
@auth.login_required
def get_participant(id):
    participant = models.Participant.query.filter_by(id=id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    return  participant_schema.jsonify(participant)

@app.route('/api/participant/<int:id>/image', methods=['POST'])
@auth.login_required
@requires_roles('USER','ADMIN')
def set_participant_image(id):
    if(g.user.id != id):
        raise RestException(RestException.NOT_YOUR_ACCOUNT, 403)
    file = request.files.get('image')
    extension = file.filename.rsplit('.', 1)[1].lower()
    participant = models.Participant.query.filter_by(id=id).first()
    filename = file_server.save_participant_image(file, participant, extension, file.content_type)
    participant.image_file = filename
    db.session.add(participant)
    db.session.commit()
    return filename

@app.route('/api/logo/<string:id>/<string:tracking_id>/logo.jpg')
def get_logo_tracking(id, tracking_id):
    email_log = models.EmailLog.query.filter_by(participant_id=id, tracking_code=tracking_id).first()
    if(email_log) :
        email_log.opened = True
        email_log.date_opened = datetime.datetime.now()
        db.session.add(email_log)
        db.session.commit()


    return send_file("static/images/logo.jpg", mimetype='image/jpg')

@app.route('/api/participant/<int:id>', methods=['DELETE'])
@auth.login_required
@requires_roles('ADMIN')
def remove_participant(id):
    participant = models.Participant.query.filter_by(id=id).first()
    db.session.delete(participant)
    db.session.commit()
    return ""

@app.route('/api/participant/<int:participant_id>/session/<int:session_id>', methods=['GET'])
@auth.login_required
def get_registration(participant_id, session_id):
    participant = models.Participant.query.filter_by(id=participant_id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    session = models.Session.query.filter_by(id=session_id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    participant_session = participant.getParticipantSession(session)
    if(participant_session is None):
        return jsonify(error=404, text=str("Participant is not registered for this session.")), 404

    return(jsonify(participant_session_db_schema.dump(participant_session).data))

@app.route('/api/participant/search', methods=['POST'])
@auth.login_required
def search_participant():
    request_data = request.get_json()
    search = models.SearchSchema().load(request_data).data
    try:
        results = elastic_index.search_participants(search)
    except elasticsearch.ElasticsearchException as e:
        raise RestException(RestException.ELASTIC_ERROR)
    search.total = results.hits.total
    participants = []
    for hit in results:
        participant = models.Participant.query.filter_by(id=hit.id).first()
        participants.append(participant)
    search.participants = participant_schema.dump(participants, many=True).data
    return models.SearchSchema().jsonify(search)
