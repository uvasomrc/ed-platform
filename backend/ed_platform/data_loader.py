import sys
from flask import json
from flask_script import Command, Option

from ed_platform import models

class DataLoader():
    "loads a json file into the database. A poor man's seed program, since I couldn't find one.  Handles relationships."
    file = "example_data.json"
    load_order = ["Track", "Workshop", "TrackWorkshop","Session","Participant","ParticipantSession", "EmailMessage", "EmailLog"]

    def __init__(self, db, file = None):
        self.db = db
        self.file = file

    def load(self, file = None):
        name_map = {}  # maps names to their unique id after added to the db.
        if(file == None): file = self.file
        with open(file) as data_file:
            tables = json.load(data_file)
            for key in self.load_order:
                try:
                    schema_class_ = getattr(models, key + "DBSchema")
                except:
                    continue
                schema = schema_class_ ()
                for i in tables[key]:
                    # replace the name with a unique id when encountered.
                    for k,v in i["data"].items():
                        if isinstance(v, str) and v in name_map:
                            i["data"][k] = name_map[v]
                        if isinstance(v, (list, tuple)):
                            new_list = []
                            for x in v:
                                if x in name_map:
                                    new_list.append(name_map[x])
                                else:
                                    new_list.append(x)
                            i["data"][k] = new_list
                    try:
                        result = schema.load(i["data"])
                    except Exception as e:
                        print ("Eerror:" + str(e))
                        print("Failed to import data:" + str(i["data"]))
                        exit(1)
                    if len(result.errors) > 0:
                        print("Failed to load " + key + ".  With errors:" + str(result.errors))
                        exit(1)
                    item = result.data
                    self.db.session.add(item)
                    self.db.session.commit()
                    if hasattr(item, "id"):
                        name_map[i["name"]] = item.id
                print('Added %i to %s' % (len(tables[key]), key))

    def clear(self):
        for key in reversed(self.load_order):
            model_class = getattr(models, key)
            try:
                model_class.query.delete()
            except:
                print("Failed to delete " + key + ": " + sys.exc_info()[0])
                pass # We're just clearing the data out, if it doesn't
                     # exist yet no worries.
            self.db.session.commit()

    def index(self, index):
        '''Take all the data in the database and reindex it.'''
        index.clear()
        workshops = models.Workshop.query.all()
        index.load_all(workshops)
