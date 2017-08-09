import os
from app import app, db
import unittest
import tempfile

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
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


if __name__ == '__main__':
    unittest.main()