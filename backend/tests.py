import unittest
from flask import json, request
from ed_platform import app, db, data_loader, models


class TestCase(unittest.TestCase):

    test_uid = "dhf8rtest"

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
        self.assert_success(rv)
        rd = json.loads(rv.get_data(as_text=True))
        return rd

    def add_test_workshop(self):
        data = {'image_file': 'workshop_one.jpg',
                'title': 'This is a test workshop',
                'description': 'This is the test description',
                }
        rv = self.app.post('/api/workshop', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def add_test_session(self, workshop_id):
        data = {
            "workshop": workshop_id,
            "date_time": "2017-11-11T18:30:00.000Z",
            "duration_minutes": "60",
            "instructor_notes": "This is a note from the instructor",
            "max_attendees": 2
        }
        rv = self.app.post('/api/session', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def add_test_participant(self):
        data = {
            "display_name": "Peter Dinklage",
            "email_address": "tyrion@got.com",
            "phone_number": "+15554570024",
            "created": "2017-08-28T16:09:00.000Z",
            "bio": "Award-winning actor Peter Dinklage has earned critical acclaim for his work in the 2003 film 'The Station Agent' and on the hit television series 'Game of Thrones.'"
        }
        rv = self.app.post('/api/participant', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def logged_in_headers(self):
        headers = {'uid': self.test_uid, 'givenName': 'Daniel', 'mail': 'dhf8r@virginia.edu'}
        rv = self.app.get("/api/login", headers=headers, follow_redirects=True,
                          content_type="application/json")
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()

        return dict(Authorization='Bearer ' + participant.encode_auth_token().decode())

    def get_current_participant(self):
        """ Test for the current participant status """
        # Create the user
        headers = {'uid': self.test_uid, 'givenName': 'Daniel', 'mail': 'dhf8r@virginia.edu'}
        rv = self.app.get("/api/login", headers=headers, follow_redirects=True,
                      content_type="application/json")
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()

        # Now get the user back.
        response = self.app.get('/api/auth',headers=dict(
                       Authorization='Bearer ' +
                        participant.encode_auth_token().decode()
            )
        )
        self.assert_success(response)
        return json.loads(response.data.decode())


    def assert_success(self, rv):
        self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                        "BAD Response:" + rv.status + ".")

    def assert_failure(self, rv, code=""):
        self.assertFalse(rv.status_code >= 200 and rv.status_code < 300,
                        "Incorrect Valid Response:" + rv.status + ".")
        if(code != ""):
            errors = json.loads(rv.get_data(as_text=True))
            self.assertEquals(errors["code"],code)

    def get_workshop(self, id):
        rv = self.app.get('/api/workshop/%i' %id,
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

    def test_set_workshops_for_track(self):
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

    def test_remove_track(self):
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

        rv = self.app.delete(track["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)

        rv = self.app.get(workshop["_links"]["tracks"], follow_redirects=True)
        self.assert_success(rv)
        tracks = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(tracks["tracks"]))

    def test_add_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        self.assertEqual("This is a note from the instructor", session["instructor_notes"])

        self.assertEqual(workshop["id"], session["workshop"]["id"])

    def test_get_sessions(self):
        url = '/api/session'
        print("The url is " + url)
        rv = self.app.get(url, follow_redirects=True)
        self.assert_success(rv)

    def test_get_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        url = '/api/session/%i' %session["id"]
        print("The url is " + url)
        rv = self.app.get(url, follow_redirects=True)
        self.assert_success(rv)
        session = json.loads(rv.get_data(as_text=True))
        self.assertEqual("This is a note from the instructor", session["instructor_notes"])
        self.assertEqual(workshop["id"], session["workshop"]["id"])
        self.assertTrue("_links" in session, "Session Has Links.")

    def test_get_workshop_sessions(self):
        workshop = self.add_test_workshop()
        session1 = self.add_test_session(workshop["id"])
        session2 = self.add_test_session(workshop["id"])
        self.assertIsNotNone(workshop["_links"]["sessions"])
        rv = self.app.get(workshop["_links"]["sessions"], follow_redirects=True)
        self.assert_success(rv)
        session_list = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(session_list["sessions"]))

    def test_remove_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        rv = self.app.delete(session["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get(session["_links"]["self"], follow_redirects=True)
        self.assertEqual(404, rv.status_code)

    def test_remove_workshop_with_active_sessions(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        rv = self.app.delete(workshop["_links"]["self"], follow_redirects=True)
        self.assertEqual(409, rv.status_code)
        rv = self.app.delete(session["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.delete(workshop["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)

    def test_add_participant(self):
        participant = self.add_test_participant()

    def test_get_participant(self):
        participant = self.add_test_participant()
        rv = self.app.get(participant["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)

    def test_delete_participant(self):
        participant = self.add_test_participant()
        rv = self.app.delete(participant["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get(participant["_links"]["self"], follow_redirects=True)
        self.assertEqual(404, rv.status_code)

    def test_get_all_participants(self):
        rv = self.app.get('/api/participant', follow_redirects=True)
        self.assert_success(rv)
        ps = json.loads(rv.get_data(as_text=True))
        self.assertTrue(len(ps["participants"]) > 0)

    def test_register(self):
        participant = self.get_current_participant()
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop)
        rv = self.app.post("/api/session/%i/register" % (session["id"]))
        self.assert_failure(rv, code="token_invalid")
        rv = self.app.post("/api/session/%i/register" % (session["id"]), headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get(participant["_links"]["sessions"], follow_redirects=True)
        self.assert_success(rv)
        sessions = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(sessions["sessions"]))
        session2 = self.add_test_session(workshop)
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.get(participant["_links"]["sessions"], follow_redirects=True)
        sessions = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(sessions["sessions"]), "adding a second session three times, we still only have two sessions")

    def test_max_participants(self):
        p1 = self.add_test_participant()
        p2 = self.add_test_participant()
        participant1 = models.Participant.query.filter_by(id=p1["id"]).first()
        participant2 = models.Participant.query.filter_by(id=p2["id"]).first()
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop)
        sessionModel = models.Session.query.filter_by(id=session['id']).first()
        sessionModel.max_attendees = 2
        participant1.register(sessionModel)
        participant2.register(sessionModel)
        db.session.merge(sessionModel)
        db.session.merge(participant1)
        db.session.merge(participant2)
        db.session.commit()

        rv = self.app.post("/api//session/%i/register" % session["id"], headers=self.logged_in_headers())
        self.assert_failure(rv)

    def test_unregister(self):
        participant = self.add_test_participant()
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop)
        self.app.post("/api/session/%i/register" % session["id"], headers=self.logged_in_headers())
        self.app.delete("/api/session/%i/register" % session["id"], headers=self.logged_in_headers())
        rv = self.app.get("/api/auth", headers=self.logged_in_headers(), follow_redirects=True)
        participant = json.loads(rv.get_data(as_text=True))
        print("The participant is:" + str(participant))
        self.assertEqual(0, len(participant["participant_sessions"]))

    def test_review(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop)
        rv = self.app.post("/api/session/%i/register" % session["id"], headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get("/api/session/%i/register" % session["id"], headers=self.logged_in_headers())
        self.assert_success(rv)
        reg = json.loads(rv.get_data(as_text=True))
        reg["review_score"] = 5
        reg["review_comment"] = "An excellent class"
        rv = self.app.put('/api/session/%i/register' %  session["id"],
                            headers = self.logged_in_headers(),
                            data=json.dumps(reg), follow_redirects=True,
                            content_type="application/json")
        reg2 = json.loads(rv.get_data(as_text=True))
        self.assertEqual(5, reg2["review_score"])
        self.assertEqual("An excellent class", reg2["review_comment"])

    # Authentication
    # ---------------------------------------
    def test_auth_token(self):
        participant = models.Participant (
            uid="dhf8r"
        )
        auth_token = participant.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual("dhf8r", participant.decode_auth_token(auth_token))

    def test_decode_auth_token(self):
        participant = models.Participant(
            uid="dhf8r"
        )
        auth_token = participant.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))


    def test_auth_creates_participant(self):
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()
        self.assertIsNone(participant)

        headers={'uid':self.test_uid,'givenName':'Daniel','mail':'dhf8r@virginia.edu'}
        rv = self.app.get("/api/login",  headers=headers, follow_redirects=True,
                           content_type="application/json")
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()
        self.assertIsNotNone(participant)
        self.assertIsNotNone(participant.display_name)
        self.assertIsNotNone(participant.email_address)
        self.assertIsNotNone(participant.created)

    def test_current_participant_status(self):
        data = self.get_current_participant()
        self.assertTrue("id" in data)
        self.assertTrue(data['email_address'] == 'dhf8r@virginia.edu')
        self.assertTrue(data['uid'] == self.test_uid)
        self.assertTrue(data['display_name'] == 'Daniel')

    def test_current_participant_details(self):

        # Register user to a session.
        self.get_current_participant()
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()
        session = models.Session.query.first()
        participant.register(session)
        db.session.merge(participant)
        db.session.commit()

        data = self.get_current_participant()
        self.assertTrue('participant_sessions' in data)

    def test_session_knows_instructors(self):
        session = models.Session.query.first()
        self.assertIsNotNone(session.instructors())
        self.assertTrue(len(session.instructors()) > 0)




if __name__ == '__main__':
    unittest.main()
