from flask import json
from flask_script import Command, Option

from ed_platform import models

class DataLoader():
    "loads a json file into the database. A poor man's seed program, since I couldn't find one.  Handles relationships."
    file = "example_data.json"
    load_order = ["Track", "Workshop", "TrackWorkshop","Session","Participant","ParticipantSession"]

    def __init__(self, db, file = None):
        self.db = db
        self.file = file

    def load(self, file = None):
        name_map = {}  # maps names to their unique id after added to the db.
        if(file == None): file = self.file
        with open(file) as data_file:
            tables = json.load(data_file)
            for key in self.load_order:
                schema_class_ = getattr(models, key + "DBSchema")
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
                    result = schema.load(i["data"])
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
            model_class.query.delete()

