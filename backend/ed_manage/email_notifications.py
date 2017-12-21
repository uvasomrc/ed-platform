from flask_script import Command, Option

from ed_platform import data_loader


class EmailNotifications(Command):

    """Loops through workshops, notifying participants of various events """

    def __init__(self, db, file):
        object.__init__(self)
        self.db = db
        self.file = file
        self.emails = emails
        self.loader = data_loader.DataLoader(db, file)

    option_list = (
        Option('--file', '-f', dest='file'),
    )

    def run(self, file=None):
        if file == None: file = self.file
        print("loading data from " + file)
        self.loader.load(file)