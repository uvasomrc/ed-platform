import magic
from flask_script import Command, Option
import os

from ed_platform import models, profile_photos


class LocalFilesToS3(Command):
    """Loop through images for Tracks and Workshops, uploading them to S3 and
        setting the correct path for those images. """

    def __init__(self, fileServer, db):
        object.__init__(self)
        self.fileServer = fileServer
        self.db = db
        self.mime = magic.Magic(mime=True)

    def run(self):
        self.move_track_image()
        self.move_participant_image()

    def move_track_image(self):
        tracks = models.Track.query.all()
        for track in tracks:
            path = ""
            if os.path.isfile('ed_platform/static/' + track.image_file):
                path = './ed_platform/static/' + track.image_file
            elif os.path.isfile(profile_photos.path(track.image_file)):
                path = profile_photos.path(track.image_file)
            else:
                continue;
            extension = path.rsplit('.', 1)[1].lower()
            mime_type = self.mime.from_file(path)
            data = open(path, 'rb')
            s3_path = self.fileServer.save_track_image(data, track, extension, mime_type)
            track.image_file = s3_path
            self.db.session.add(track)
            self.db.session.commit()

    def move_participant_image(self):
        participants = models.Participant.query.all()
        for participant in participants:
            path = ""
            if participant.image_file is None:
                continue
            elif os.path.isfile('ed_platform/static/' + participant.image_file):
                path = './ed_platform/static/' + participant.image_file
            elif os.path.isfile(profile_photos.path(participant.image_file)):
                path = profile_photos.path(participant.image_file)
            else:
                continue;
            extension = path.rsplit('.', 1)[1].lower()
            mime_type = self.mime.from_file(path)
            data = open(path, 'rb')
            s3_path = self.fileServer.save_participant_image(data, participant, extension, mime_type)
            participant.image_file = s3_path
            self.db.session.add(participant)
            self.db.session.commit()



