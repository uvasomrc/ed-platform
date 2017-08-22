from flask import json
from flask_script import Command, Option

from ed_platform import models


class LoadData(Command):
    "loads a json file into the database. A poor man's seed program, since I couldn't find one.  Handles relationships."

    def __init__(self, db, file):
        self.db = db
        self.file = file

    option_list = (
        Option('--file', '-f', dest='file'),
    )

    def run(self, file=None):
        name_map = {} # maps names to their unique id after added to the db.

        if(file == None): file = self.file
        print("loading data from " + file)
        with open(file) as data_file:
            tables = json.load(data_file)
            for key in tables.keys():
                schema_class_ = getattr(models, key + "Schema")
                schema = schema_class_ ()
                for i in tables[key]:
                    # replace the name with a unique id when encountered.
                    print(str(i["data"]))
                    for k,v in i["data"].items():
                        if v in name_map:
                            i["data"][k] = name_map[v]
                    item = schema.load(i["data"]).data
                    self.db.session.add(item)
                    self.db.session.commit()
                    name_map[i["name"]] = item.id
                    print ("The map is " + str(name_map))
                print('Added %i to %s' % (len(tables[key]), key))


class ClearData(Command):
    "Deletes all data from the database"
    def __init__(self, db):
        self.db = db

    def run(self):
        print("Deleting data." )
        models.Track.query.delete()
        self.db.session.commit()

