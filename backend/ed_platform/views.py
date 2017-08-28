from flask import jsonify, request, send_file
from ed_platform import app, db, models

track_schema = models.TrackAPISchema()
workshop_schema = models.WorkshopAPISchema()
session_schema = models.SessionAPISchema()

track_db_schema = models.TrackDBSchema()
workshop_db_schema = models.WorkshopDBSchema()
session_db_schema = models.SessionDBSchema()

@app.route('/api', methods=['GET'])
def root():
    return "ED Platform API"

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


