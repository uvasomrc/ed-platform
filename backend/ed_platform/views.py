from flask import jsonify, request, send_file, session, redirect
from ed_platform import app, db, models, sso, RestException

user_schema = models.UserSchema()
track_schema = models.TrackAPISchema()
workshop_schema = models.WorkshopAPISchema()
session_schema = models.SessionAPISchema()
participant_schema = models.ParticipantAPISchema()

track_db_schema = models.TrackDBSchema()
workshop_db_schema = models.WorkshopDBSchema()
session_db_schema = models.SessionDBSchema()
participant_db_schema = models.ParticipantDBSchema()
participant_session_db_schema = models.ParticipantSessionDBSchema()


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



@app.route('/api/auth')
def status():
    auth_header = request.headers.get('Authorization')
    if auth_header and len(auth_header.split(" ")) > 1:
            auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = models.Participant.decode_auth_token(auth_token)
        participant = models.Participant.query.filter_by(uid=resp).first()
        return jsonify(participant_schema.dump(participant).data)
    else:
        raise RestException(RestException.TOKEN_MISSING)


@app.route('/api/logout')
def logout():
    #fixme: Logout should invalidate the auth token.
    session.pop('user')
    return redirect('/api/')



# Tracks
# *****************************

@app.route('/api/track', methods=['POST'])
def create_track():
    request_data = request.get_json()
    new_track = track_db_schema.load(request_data).data
    db.session.add(new_track)
    db.session.commit()
    return track_schema.jsonify(new_track)


@app.route('/api/track', methods=['GET'])
def get_tracks():
    tracks = list(map(lambda t: track_schema.dump(t).data, models.Track.query.all()))
    return jsonify({"tracks": tracks})


@app.route('/api/track/<int:track_id>')
def get_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if(track is None):
        return jsonify(error=404, text=str("no such track.")), 404
    return track_schema.jsonify(track)

@app.route('/api/track/<int:track_id>', methods=['DELETE'])
def remove_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    if(track is None):
        return jsonify(error=404, text=str("no such track.")), 404
    for tw in track.track_workshops:
        db.session.delete(tw)
    db.session.delete(track)
    return ""


@app.route('/api/track/<int:track_id>/workshops')
def get_track_workshops(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    track_workshops = track.track_workshops
    workshops = list(map(lambda t: workshop_schema.dump(t.workshop).data, track_workshops))
    return jsonify({"workshops": workshops})


@app.route('/api/track/<int:id>/workshops', methods=['PATCH'])
def set_track_workshops(id):
    request_data = request.get_json()
    workshops = workshop_db_schema.load(request_data["workshops"], many=True).data
    track = models.Track.query.filter_by(id=id).first()
    track_workshops = []
    order = 0
    for workshop in workshops:
        track_workshops.append(models.TrackWorkshop(track_id=track.id, workshop_id=workshop.id, order=order))
        order += 1
    track.track_workshops = track_workshops
    db.session.commit()
    workshops = list(map(lambda t: workshop_schema.dump(t.workshop).data, track_workshops))
    return jsonify({"workshops": workshops})


@app.route('/api/track/<int:track_id>/image')
def get_track_image(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    return send_file("static/" + track.image_file, mimetype='image/png')


# Workshop
# *****************************


@app.route('/api/workshop')
def get_workshops():
    workshops = list(map(lambda t: workshop_schema.dump(t).data,
                         models.Workshop.query.all()))
    return jsonify({"workshops": workshops})


@app.route('/api/workshop', methods=['POST'])
def create_workshop():
    request_data = request.get_json()
    new_workshop = workshop_db_schema.load(request_data).data
    db.session.add(new_workshop)
    db.session.commit()
    return workshop_schema.jsonify(new_workshop)


@app.route('/api/workshop/<int:id>')
def get_workshop(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop is None):
        return jsonify(error=404, text=str("no such workshop.")), 404
    return workshop_schema.jsonify(workshop)


@app.route('/api/workshop/<int:id>', methods=['DELETE'])
def remove_workshop(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    if(workshop is None): return ""
    if(len(workshop.sessions) > 0):
        return jsonify(error=409, text=str("workshop has sessions. Can't delete.")), 409
    db.session.delete(workshop)
    db.session.commit()
    return ""


@app.route('/api/workshop/<int:id>/tracks')
def get_workshop_tracks(id):
    workshop = models.Workshop.query.filter_by(id=id).first()
    tracks = list(map(lambda t: track_schema.dump(t.track).data, workshop.track_workshops))
    return jsonify({"tracks": tracks})


@app.route('/api/workshop/<int:id>/sessions', methods=['GET'])
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
def get_sessions():
    sessions = list(map(lambda t: session_schema.dump(t).data,
                         models.Session.query.all()))
    return jsonify({"sessions": sessions})


@app.route('/api/session', methods=['POST'])
def create_session():
    request_data = request.get_json()
    new_session = session_db_schema.load(request_data).data
    db.session.add(new_session)
    db.session.commit()
    return session_schema.jsonify(new_session)

@app.route('/api/session/<int:id>', methods=['GET'])
def get_session(id):
    session = models.Session.query.filter_by(id=id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    return  session_schema.jsonify(session)

@app.route('/api/session/<int:id>', methods=['DELETE'])
def remove_session(id):
    session = models.Session.query.filter_by(id=id).first()
    db.session.delete(session)
    db.session.commit()
    return ""

# Participants
# *****************************

@app.route('/api/participant', methods=['GET'])
def get_participants():
    participants = list(map(lambda t: participant_schema.dump(t).data,
                         models.Participant.query.all()))
    return jsonify({"participants": participants})

@app.route('/api/participant', methods=['POST'])
def create_participant():
    request_data = request.get_json()
    participant = participant_db_schema.load(request_data).data
    db.session.add(participant)
    db.session.commit()
    return participant_schema.jsonify(participant)

@app.route('/api/participant/<int:id>', methods=['GET'])
def get_participant(id):
    participant = models.Participant.query.filter_by(id=id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    return  participant_schema.jsonify(participant)

@app.route('/api/participant/<int:id>/image')
def get_participant_image(id):
    participant = models.Participant.query.filter_by(id=id).first()
    return send_file("static/" + participant.image_file, mimetype='image/png')

@app.route('/api/participant/<int:id>', methods=['DELETE'])
def remove_participant(id):
    participant = models.Participant.query.filter_by(id=id).first()
    db.session.delete(participant)
    db.session.commit()
    return ""

@app.route('/api/participant/<int:id>/sessions', methods=['GET'])
def get_participant_sessions(id):
    participant = models.Participant.query.filter_by(id=id).first()
    sessions = list(map(lambda ps: session_schema.dump(ps.session).data, participant.participant_sessions))
    return jsonify({"sessions":sessions})


@app.route('/api/participant/<int:participant_id>/session/<int:session_id>', methods=['GET'])
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


@app.route('/api/participant/<int:participant_id>/session/<int:session_id>', methods=['POST'])
def register(participant_id, session_id):
    participant = models.Participant.query.filter_by(id=participant_id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    session = models.Session.query.filter_by(id=session_id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    participant.register(session)

    db.session.merge(participant)
    db.session.commit()
    return (jsonify(participant_session_db_schema.dump(participant.getParticipantSession(session)).data))

@app.route('/api/participant/<int:participant_id>/session/<int:session_id>', methods=['PUT'])
def review(participant_id, session_id):

    reg = models.ParticipantSession.query.filter_by(participant_id=participant_id,
                                                    session_id=session_id).first()
    updates = request.get_json()
    reg.review_score = updates["review_score"]
    reg.review_comment = updates["review_comment"]

    db.session.commit()
    return (jsonify(participant_session_db_schema.dump(reg).data))


@app.route('/api/participant/<int:participant_id>/session/<int:session_id>', methods=['DELETE'])
def unregister(participant_id, session_id):
    participant = models.Participant.query.filter_by(id=participant_id).first()
    if(participant is None):
        return jsonify(error=404, text=str("no such participant.")), 404
    session = models.Session.query.filter_by(id=session_id).first()
    if(session is None):
        return jsonify(error=404, text=str("no such session.")), 404
    participant_session = participant.getParticipantSession(session)
    if(participant_session is not None):
        db.session.delete(participant_session)
        db.session.commit()
    return ""

