import boto3


class FileServer:

    def __init__(self, app):
        self.s3 = boto3.resource('s3')
        self.bucket = app.config['S3']['bucket']

    def _save_file(self, data, filename, mime_type):
        self.s3.Bucket(self.bucket).put_object(Key=filename, Body=data, ACL='public-read',
                                               ContentType=mime_type)
        return self._get_remote_path(filename)

    def _get_remote_path(self, filename):
        return "https://s3.amazonaws.com/{0}/{1}".format(self.bucket, filename)

    def save_track_image(self, data, track, file_extension, mime_type):
        path = "edplatform/tracks/%s.%s" % (track.id, file_extension)
        file_name = self._save_file(data, path, mime_type)
        return file_name

    def save_participant_image(self, data, participant, file_extension, mime_type):
        path = "edplatform/participants/%s.%s" % (participant.id, file_extension)
        file_name = self._save_file(data, path, mime_type)
        return file_name
