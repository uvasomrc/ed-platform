from flask import Flask, jsonify, request
# from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'This is very basic starting point for the Ed-Platform project!'


@app.route('/track', methods=['POST'])
def create_track():
    request_data = request.get_json()
    new_track = models.Track(
        request_data['image_file'],
        request_data['title'],
        request_data['description'])
    db.session.add(new_track)
    db.session.commit()
    return jsonify(new_track.as_dict())


@app.route('/track', methods=['GET'])
def get_tracks():
    return jsonify({'tracks': models.Track.query.all()})


@app.route('/track/<int:track_id>')
def get_track(track_id):
    track = models.Track.query.filter_by(id=track_id).first()
    return jsonify(track.as_dict())


@app.route('/track/<string:name>/course', methods=['POST'])
def create_course_in_track(name):
    print(name)
    pass


@app.route('/track/<string:name>/item')
def get_courses_in_track(name):
    print(name)
    pass


if __name__ == '__main__':
    app.run()

import models