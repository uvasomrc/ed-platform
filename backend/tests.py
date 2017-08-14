import unittest

from flask import json

from ed_platform import app,db,models


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_envvar('APP_CONFIG_FILE')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_silly(self):
        rv = self.app.get('/')
        print(rv.data)
        assert b'This is very basic starting point for the Ed-Platform project!' in rv.data

    def test_add_track(self):
        new_track = models.Track(image_file='track_one.jpg',
                                 title='This is the title',
                                 description='This is the description')
        data = json.dumps(new_track.as_dict())

        rv = self.app.post('/track', data=data, follow_redirects=True,
                           content_type="application/json")

        rd = json.loads(rv.get_data(as_text=True))
        assert rd['title'] == "This is the title"
        assert rd['description'] == "This is the description"
        assert rd['image_file'] == "track_one.jpg"
        assert rd["id"] is not None

        rv2 = self.app.get('/track/' + str(rd["id"]))
        assert b'track_one.jpg' in rv2.data
        assert b'This is the title' in rv2.data
        assert b'This is the description' in rv2.data


if __name__ == '__main__':
    unittest.main()