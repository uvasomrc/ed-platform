import unittest
from flask import json
from ed_platform import app, db, data_loader, models


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile('../config/testing.py')

        self.app = app.test_client()
        db.create_all()
        self.ctx = app.test_request_context()
        self.ctx.push()
        loader = data_loader.DataLoader(db)
        loader.load("example_data.json")

        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)

    def tearDown(self):
        self.ctx.pop()
        db.drop_all()
        pass

    def test_base(self):
        rv = self.app.get('/api')
        print(rv.data)
        assert b'ED Platform API' in rv.data

    def add_test_track(self):
        data = {'image_file': 'track_one.jpg',
                'title': 'This is the title',
                'description': 'This is the description'}
        rv = self.app.post('/api/track', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        rd = json.loads(rv.get_data(as_text=True))
        return rd

    def add_test_workshop(self):
        data = {'image_file': 'workshop_one.jpg',
                'title': 'This is a test workshop',
                'description': 'This is the test description',
                }
        rv = self.app.post('/api/workshop', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        return json.loads(rv.get_data(as_text=True))

    def get_workshop(self, id):
        rv = self.app.get('/api/workshop/%id' %id,
                           follow_redirects=True,
                           content_type="application/json")
        return json.loads(rv.get_data(as_text=True))


    def test_add_track(self):
        rd = self.add_test_track()
        assert rd['title'] == "This is the title"
        assert rd['description'] == "This is the description"
        assert rd["id"] is not None

        rv2 = self.app.get('/api/track/' + str(rd["id"]))
        assert b'This is the title' in rv2.data
        assert b'This is the description' in rv2.data

    def test_get_tracks(self):
        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        assert len(all_tracks["tracks"]) > 1
        track1 = all_tracks["tracks"][0]
        self.assertTrue("title" in track1.keys())
        self.assertTrue("description" in track1.keys())
        self.assertTrue(len(track1["_links"]["workshops"]) > 0)

    def test_sample_data_load(self):
        track = models.Track.query.filter_by(id=1).first()
        assert track.title == "Learning Python The Hard Way"

    def test_add_workshop(self):
        workshop = self.add_test_workshop()
        self.assertEqual("This is a test workshop", workshop["title"])

    def test_add_workshop_to_track(self):
        track    = self.add_test_track()
        workshop = self.add_test_workshop()
        data = json.dumps({"workshops":[workshop]})
        url = '/api/track/%i/workshops' % track['id']

        response = self.app.patch(url,
                            follow_redirects=True,
                            data = data,
                            content_type="application/json")

        workshops = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(workshops["workshops"]), 1)

if __name__ == '__main__':
    unittest.main()
