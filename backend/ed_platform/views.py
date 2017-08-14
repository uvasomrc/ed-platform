from flask import jsonify, request, send_file
from ed_platform import app, db, models


@app.route('/')
def hello_world():
    return 'This is very basic starting point for the Ed-Platform project!'


@app.route('/track', methods=['POST'])
def create_track():
    request_data = request.get_json()
    new_track = models.Track.from_dict(request_data)
    db.session.add(new_track)
    db.session.commit()
    return jsonify(new_track.as_dict())


@app.route('/track', methods=['GET'])
def get_tracks():
    tracks = list(map(lambda t: t.as_dict(), models.Track.query.all()))
    return jsonify({"tracks":tracks})

@app.route('/track/<int:track_id>')
def get_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    return jsonify(track.as_dict())

@app.route('/track/image/<int:track_id>')
def get_track_image(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    return send_file("static/" + track.image_file, mimetype='image/png')

@app.route('/track/<string:name>/course', methods=['POST'])
def create_course_in_track(name):
    print(name)
    pass


@app.route('/track/<string:name>/item')
def get_courses_in_track(name):
    print(name)
    pass
