from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is very basic starting point for the Ed-Platform project!'

tracks = [
    {'name':'Python',
        'courses': [
            {'name': 'Intro to Python',
            'instructor': 'Dan'},
            {'name': 'Python REST APIs',
            'instructor': 'Neal'}
        ]
    }
    ]

@app.route('/track', methods=['POST'])
def create_track():
    request_data = request.get_json()
    new_track = {
        'name': request_data['name'],
        'courses': []
    }
    tracks.append(new_track)
    return jsonify(new_track)

@app.route('/track', methods=['GET'])
def get_tracks():
    return jsonify({'tracks': tracks})

@app.route('/track/<string:name>')
def get_track(name):
    for t in tracks :
        if(t['name'] == name):
            return jsonify(t)
    return (jsonify({"Error":"No tracks match the given name."}))


@app.route('/track/<string:name>/course',methods=['POST'])
def create_course_in_track(name):
    pass

@app.route('/track/<string:name>/item')
def get_courses_in_track(name):
    pass


if __name__ == '__main__':
    app.run()
