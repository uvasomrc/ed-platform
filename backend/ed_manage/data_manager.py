from flask_script import Command, Option

from ed_platform import data_loader


class LoadData(Command):
    """loads a json file into the database. A poor man's seed program, since I couldn't find one. """

    def __init__(self, db, file):
        object.__init__(self)
        self.db = db
        self.file = file
        self.loader = data_loader.DataLoader(db, file)

    option_list = (
        Option('--file', '-f', dest='file'),
    )

    def run(self, file=None):
        if file == None: file = self.file
        print("loading data from " + file)
        self.loader.load(file)


class ClearData(Command):
    """Deletes all data from the database"""
    def __init__(self, db):
        object.__init__(self)
        self.db = db
        self.loader = data_loader.DataLoader(db)

    def run(self):
        print("Deleting data.")
        self.loader.clear()
