import unittest
from flask import json
from ed_platform import app,db,data_loader
from flask_script import Manager


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

    def test_add_track(self):
        data = {'image_file':'track_one.jpg',
                'title':'This is the title',
                'description':'This is the description'}

        rv = self.app.post('/api/track', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")

        rd = json.loads(rv.get_data(as_text=True))
        assert rd['title'] == "This is the title"
        assert rd['description'] == "This is the description"
        assert rd['image_file'] == "track_one.jpg"
        assert rd["id"] is not None

        rv2 = self.app.get('/api/track/' + str(rd["id"]))
        assert b'track_one.jpg' in rv2.data
        assert b'This is the title' in rv2.data
        assert b'This is the description' in rv2.data

    def test_track_has_workshops(self):
        pass

if __name__ == '__main__':
    unittest.main()