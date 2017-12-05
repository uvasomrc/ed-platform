import datetime

import elasticsearch
import magic
import os
from flask import jsonify, request, send_file, session, redirect, g, render_template, json
from ed_platform import app, db, models, sso, RestException, emails, elastic_index, profile_photos, discourse
from flask_httpauth import HTTPTokenAuth

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
    return models.WorkshopAPISchema().jsonify(g.user.getWorkshops(),many=True)

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


def update_tracks_for_participant(track, participant):
    for code in track:
        code.status = participant.get_status_for_code(code)

@app.route('/api/track', methods=['GET'])
@auth.login_required
def get_tracks():
    tracks = list(map(lambda t: track_schema.dump(t).data, models.Track.query.all()))
    return jsonify({"tracks": tracks})


@app.route('/api/track/<int:track_id>')
@auth.login_required
def get_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if(track is None):
        return jsonify(error=404, text=str("no such track.")), 404
    return track_schema.jsonify(track)

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


@app.route('/api/track/<int:track_id>/image')
def get_track_image(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if( not track.image_file):
        raise RestException(RestException.NOT_FOUND)
    try:
        return send_file("static/" + track.image_file, mimetype='image/png')
    except FileNotFoundError:
        raise RestException(RestException.NOT_FOUND)

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
            fields = ['date_time', 'duration_minutes', 'location', 'instructor_notes', 'max_attendees']
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

    if(request_data["discourse_enabled"] and new_workshop.discourse_topic_id is None):
        topic = discourse.createTopic(new_workshop)
        new_workshop.discourse_topic_id = topic.id

    db.session.add(new_workshop)
    db.session.commit()

    return workshop_schema.jsonify(new_workshop)

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
        return jsonify(error=409, text=str("workshop has sessions. Can't delete.")), 409
    db.session.delete(workshop)
    db.session.commit()
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
    wait_listed = False
    if(session is None):
        raise RestException(RestException.NO_SUCH_SESSION, 404)
    if(session.max_attendees <= len(session.participant_sessions)):
        wait_listed = True
        participant.wait_list(session)
    else:
        participant.register(session)
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

@app.route('/api/session/<int:id>/email', methods=['POST'])
@auth.login_required
def email_participants(id):
    instructor = g.user
    session = models.Session.query.filter_by(id=id).first()
    if(instructor != session.workshop.instructor):
        raise RestException(RestException.NOT_INSTRUCTOR)

    request_data = request.get_json()
    email = email_message_db_schema.load(request_data).data
    email.author = instructor
    email.session = session
    for ps in session.participant_sessions:
        email_log = models.EmailLog(participant=ps.participant,
                                    email_message=email)
        email.logs.append(email_log)

        # To Add: site_url, logo_url, session_url
        # instructor_image_url, workshop_date

        text_body = render_template("instructor_message.txt",
                                    session=session, participant=ps.participant,
                                    api_url=app.config['API_URL'], site_url=app.config['SITE_URL'],
                                    instructor=instructor, content=email.content)
        html_body = render_template("instructor_message.html",
                                    session=session, participant=ps.participant,
                                    instructor=instructor, content=email.content,
                                    api_url=app.config['API_URL'], site_url=app.config['SITE_URL'],
                                    tracking_code=email_log.tracking_code)

        emails.send_email("[edplatform] %s" % email.subject,
                          recipients=[ps.participant.email_address], text_body=text_body,
                          html_body=html_body)
        print(html_body)
    db.session.add(email)
    db.session.commit()

    return email_schema.jsonify(email)

@app.route('/api/session/<int:id>/messages', methods=['GET'])
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
    new_participant = participant_db_schema.load(request_data).data

    if(g.user.id != new_participant.id):
        raise RestException(RestException.NOT_YOUR_ACCOUNT, 403)

    db.session.add(new_participant)
    db.session.commit()
    return participant_schema.jsonify(new_participant)


@app.route('/api/participant/<int:id>', methods=['GET'])
@auth.login_required
def get_participant(id):
    participant = models.Participant.query.filter_by(id=id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    return  participant_schema.jsonify(participant)

@app.route('/api/participant/<int:id>/image/<int:cache_bust>')
def get_participant_image_cache_bust(id, cache_bust):
    return get_participant_image(id)

@app.route('/api/participant/<int:id>/image')
def get_participant_image(id):
    participant = models.Participant.query.filter_by(id=id).first()
    mime = magic.Magic(mime=True)
    image = ""
    mime_type = ""
    if(participant.image_file is None):
        raise RestException(RestException.NOT_FOUND, 404)
    elif(os.path.isfile('ed_platform/static/' + participant.image_file)):
        mime_type = mime.from_file('ed_platform/static/' + participant.image_file)
        image = 'static/' + participant.image_file
    elif(os.path.isfile(profile_photos.path(participant.image_file))):
        mime_type = mime.from_file(profile_photos.path(participant.image_file))
        image = profile_photos.path(participant.image_file)
    else:
        raise RestException(RestException.NOT_FOUND, 404)
    mime = magic.Magic(mime=True)
    return send_file(image, mimetype=mime_type)

@app.route('/api/participant/<int:id>/image/<int:cache_bust>', methods=['POST'])
@auth.login_required
@requires_roles('USER','ADMIN')
def set_participant_image(id, cache_bust):
    if(g.user.id != id):
        raise RestException(RestException.NOT_YOUR_ACCOUNT, 403)

    participant = models.Participant.query.filter_by(id=id).first()
    filename = profile_photos.save(request.files['image'], None, "p%i." % participant.id)
    participant.image_file = filename
    db.session.add(participant)
    db.session.commit()
    return get_participant_image(id)

@app.route('/api/logo/<string:id>/<string:tracking_id>/logo.png')
def get_logo_tracking(id, tracking_id):
    email_log = models.EmailLog.query.filter_by(participant_id=id, tracking_code=tracking_id).first()
    if(email_log) :
        email_log.opened = True
        email_log.date_opened = datetime.datetime.now()
        db.session.add(email_log)
        db.session.commit()
    return send_file("static/images/logo.png", mimetype='image/png')

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

