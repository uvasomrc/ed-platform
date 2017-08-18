from flask import json
from flask_script import Command, Option

from ed_platform import models


class LoadData(Command):
    "loads a json file into the database."

    def __init__(self, db, file):
        self.db = db
        self.file = file

    option_list = (
        Option('--file', '-f', dest='file'),
    )

    def run(self, file=None):
        if(file == None): file = self.file
        print("loading data from " + file)
        with open(file) as data_file:
            data = json.load(data_file)
            tracks = models.TrackSchema().load(data['tracks'], many=True).data
            self.db.session.add_all(tracks)
            self.db.session.commit()
            print('Added %i Tracks' % len(tracks))

class ClearData(Command):
    "Deletes all data from the database"
    def __init__(self, db):
        self.db = db

    def run(self):
        print("Deleting data." )
        models.Track.query.delete()
        self.db.session.commit()

