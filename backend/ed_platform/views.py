from flask import jsonify, request, send_file
from ed_platform import app, db, models

track_schema = models.TrackSchema()


@app.route('/api/track', methods=['POST'])
def create_track():
    request_data = request.get_json()
    new_track = models.Track.from_dict(request_data)
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
    return track_schema.jsonify(track)


@app.route('/api/track/image/<int:track_id>')
def get_track_image(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    return send_file("static/" + track.image_file, mimetype='image/png')


@app.route('/api/track/<string:name>/course', methods=['POST'])
def create_course_in_track(name):
    print(name)
    pass


@app.route('/api/track/<string:name>/item')
def get_courses_in_track(name):
    print(name)
    pass
