import datetime
import unittest

import dateutil
from flask import json, request
from flask_mail import Mail
import os

# Set enivoronment variable to testing before loading.
os.environ["APP_CONFIG_FILE"] = '../config/testing.py'

from ed_platform import app, db, data_loader, models, elastic_index
from ed_platform.emails import TEST_MESSAGES


class TestCase(unittest.TestCase):

    test_uid = "dhf8rtest"
    test_code_1 = "TEST-101"
    test_code_2 = "TEST-102"
    test_code_3 = "TEST-103"

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.ctx = app.test_request_context()
        self.ctx.push()
        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)

    def load_sample_data(self):
        db.drop_all()
        db.create_all()
        loader = data_loader.DataLoader(db)
        loader.load("./example_data.json")
        loader.index(elastic_index)
        print("Data Loaded")

    def tearDown(self):
        self.ctx.pop()
        db.drop_all()
        elastic_index.clear()
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

    def add_codes(self):
        self.add_code(self.test_code_1, "test code one desc.")
        self.add_code(self.test_code_2, "test code two desc.")
        self.add_code(self.test_code_3, "test code three desc.")

    def add_code(self, id, desc):
        data = {'id': id,
                'desc': desc}
        rv = self.app.post('/api/code', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return rv

    def assign_codes_to_track(self, track_id):
        self.add_codes()
        data = [{'id': self.test_code_1,
                'prereq': True},
                {'id': self.test_code_2,
                 'prereq': False},
                {'id': self.test_code_3,
                 'prereq': False}
                ]
        rv = self.app.patch('/api/track/%i/codes' % track_id, data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return rv


    def add_test_workshop(self):
        self.add_code(self.test_code_1, "Some description.")
        data = {'image_file': 'workshop_one.jpg',
                'title': 'This is a test workshop',
                'description': 'This is the test description',
                'code': self.test_code_1
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

    def review(self, session):
        rv = self.app.get("/api/session/%i/register" % session["id"], headers=self.logged_in_headers())
        self.assert_success(rv)
        reg = json.loads(rv.get_data(as_text=True))
        reg["review_score"] = 5
        reg["review_comment"] = "An excellent class"
        rv = self.app.put('/api/session/%i/register' % session["id"],
                          headers=self.logged_in_headers(),
                          data=json.dumps(reg), follow_redirects=True,
                          content_type="application/json")

    def get_current_participant(self):
        """ Test for the current participant status """
        # Create the user
        headers = {'uid': self.test_uid, 'givenName': 'Daniel', 'mail': 'dhf8r@virginia.edu'}
        rv = self.app.get("/api/login", headers=headers, follow_redirects=True,
                      content_type="application/json")

        participant = models.Participant.query.filter_by(uid=self.test_uid).first()

        # Now get the user back.
        response = self.app.get('/api/user',headers=dict(
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
            print(rv.get_data(as_text=True))
            errors = json.loads(rv.get_data(as_text=True))
            self.assertEqual(errors["code"],code)

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

    def test_add_code(self):
        rv = self.add_codes()
        rv = self.app.get('/api/code',
                           follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(data))
        # Codes should come back in the order they are added.
        self.assertEquals(self.test_code_1, data[0]["id"])
        self.assertEquals(self.test_code_2, data[1]["id"])
        self.assertEquals(self.test_code_3, data[2]["id"])


    def test_add_workshop_with_invalid_code(self):
        data = {'image_file': 'workshop_one.jpg',
                'title': 'This is a test workshop',
                'description': 'This is the test description',
                'code': 'there is no code like this.'
                }
        rv = self.app.post('/api/workshop', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_failure(rv)
        self.assertIn("no_such_code", rv.get_data(as_text=True))

    def test_get_code(self):
        self.add_codes()
        self.add_test_workshop()
        rv = self.app.get('/api/code/%s' % self.test_code_1,
                           follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        data = json.loads(rv.get_data(as_text=True))
        self.assertEquals(self.test_code_1, data["id"])
        self.assertEqual(1, len(data["workshops"]))

    def test_get_tracks(self):
        rd = self.add_test_track()
        self.assign_codes_to_track(rd["id"])
        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        assert len(all_tracks["tracks"]) >= 1
        track1 = all_tracks["tracks"][0]
        self.assertTrue("title" in track1.keys())
        self.assertTrue("description" in track1.keys())
        self.assertTrue("_links" in track1.keys())
        self.assertIsNotNone(track1["_links"]["self"])

        self.assertTrue("codes" in track1.keys())
        codes = track1["codes"]
        self.assertEqual(3, len(codes))
        self.assertTrue("_links" in codes[0].keys())
        self.assert_success(self.app.get(codes[0]["_links"]["self"]))

    def test_tracks_with_active_participant_know_completed_codes(self):
        participant = self.get_current_participant()
        rd = self.add_test_track()
        self.assign_codes_to_track(rd["id"])
        ws = self.add_test_workshop()
        session = self.add_test_session(ws["id"])

        # Track state for sessions is all null.
        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        code1 = all_tracks["tracks"][0]["codes"][0]
        self.assertTrue("status" in code1)
        self.assertEquals("UNREGISTERED", code1["status"])

        # Sign up for session
        rv = self.app.post("/api/session/%i/register" % (session["id"]), headers=self.logged_in_headers())

        # Get Tracks, now marked as Registered
        response = self.app.get('/api/track', headers=self.logged_in_headers())
        all_tracks = json.loads(response.get_data(as_text=True))
        code1 = all_tracks["tracks"][0]["codes"][0]
        self.assertEquals("REGISTERED", code1["status"])

        # Set the session date to the past.
        dbs = models.Session.query.filter_by(id=session["id"]).first()
        dbs.date_time = datetime.datetime.now() - datetime.timedelta(days=1)
        db.session.add(dbs)
        db.session.commit()

        # Get Tracks, now marked as waiting for attendance info
        response = self.app.get('/api/track', headers=self.logged_in_headers())
        all_tracks = json.loads(response.get_data(as_text=True))
        code1 = all_tracks["tracks"][0]["codes"][0]
        self.assertEquals("WAITING_ATTENDANCE", code1["status"])

        # Review the session (mark it as completed)
        self.review(session)

        # Get Tracks, now marked as attended
        response = self.app.get('/api/track', headers=self.logged_in_headers())
        all_tracks = json.loads(response.get_data(as_text=True))
        code1 = all_tracks["tracks"][0]["codes"][0]
        self.assertEquals("ATTENDED", code1["status"])



    def test_assign_bad_codes_to_track(self):
        rd = self.add_test_track()
        data = [{'id': "no_such_id",
                'prereq': True}]
        rv = self.app.patch('/api/track/%i/codes' % rd["id"], data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assert_failure(rv, "no_such_code")

    def test_assign_codes_to_track(self):
        rd = self.add_test_track()
        self.add_codes()
        self.assign_codes_to_track(rd["id"])
        rv = self.app.get('/api/track/%s' % rd["id"])
        track = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(track["codes"]))
        self.assertEqual(self.test_code_1, track["codes"][0]["id"])
        self.assertEqual(self.test_code_2, track["codes"][1]["id"])
        self.assertEqual(self.test_code_3, track["codes"][2]["id"])
        self.assertTrue(track["codes"][0]["prereq"])
        self.assertFalse(track["codes"][1]["prereq"])
        self.assertFalse(track["codes"][2]["prereq"])


    def test_sample_data_load(self):
        self.load_sample_data()
        track = models.Track.query.filter_by(id=1).first()
        self.assertEquals(track.title, "Python for Data Analysis")

    def test_add_workshop(self):
        workshop = self.add_test_workshop()
        self.assertEqual("This is a test workshop", workshop["title"])

    def test_remove_track(self):
        track    = self.add_test_track()

        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        self.assertEqual(1,len(all_tracks["tracks"]))

        rv = self.app.delete(track["_links"]["self"], follow_redirects=True)
        self.assert_success(rv)

        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        self.assertEqual(0,len(all_tracks["tracks"]))

    def test_add_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        self.assertEqual("This is a note from the instructor", session["instructor_notes"])

        self.assertIn(str(workshop["id"]), session["_links"]["workshop"])

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
        self.assertIn(str(workshop["id"]), session["_links"]["workshop"])
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
        participant = self.add_test_participant()
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
        rv = self.app.get(participant["_links"]["workshops"], headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        workshops = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(workshops))
        session2 = self.add_test_session(workshop)
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.post("/api/session/%i/register" % (session2["id"]), headers=self.logged_in_headers())
        rv = self.app.get(participant["_links"]["workshops"], follow_redirects=True)
        workshops = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(workshops), "adding a second session three times, we still only have two sessions")

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
        rv = self.app.get("/api/user", headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        participant = json.loads(rv.get_data(as_text=True))
        print("The participant is:" + str(participant))
        rv = self.app.get(participant["_links"]["workshops"],headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        workshops = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(workshops))

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
        self.assertTrue(data['uid'] == self.test_uid)
        self.assertTrue(data['display_name'] == 'Daniel')


    def test_get_workshops_for_current_user(self):
        self.test_add_session()
        self.get_current_participant()
        participant = models.Participant.query.filter_by(uid=self.test_uid).first()
        session = models.Session.query.first()
        participant.register(session)
        db.session.merge(participant)
        db.session.commit()

        rv = self.app.get("/api/user/workshops", follow_redirects=True,
                          headers=self.logged_in_headers(),
                          content_type="application/json")

        self.assert_success(rv)
        workshops = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(workshops))

    def test_session_knows_instructors(self):
        ws = self.add_test_workshop()
        session = self.add_test_session(ws["id"])
        participant = self.add_test_participant()

        # Mark participant as the instructor.
        rv = self.app.post("/api/session/%i/instructor/%i" % (session["id"], participant["id"]))

        session = models.Session.query.first()
        self.assertIsNotNone(session.instructors())
        self.assertTrue(len(session.instructors()) > 0)

    def test_email_participants_only_by_instructor(self):
        self.test_add_session()
        session = models.Session.query.first()
        rv = self.app.post("/api/session/%i/email" % session.id, follow_redirects=True,
                          content_type="application/json")
        self.assert_failure(rv, "token_invalid")

        rv = self.app.post("/api/session/%i/email" % session.id, headers=self.logged_in_headers())
        self.assert_failure(rv, "not_the_instructor")

    def test_email_sends_to_recipient(self):
        self.load_sample_data()
        session = models.Session.query.first()
        headers = self.logged_in_headers()
        instructor = models.Participant.query.filter_by(uid=self.test_uid).first()
        instructor.register(session, is_instructor=True)
        data = {'subject':'Test Subject', 'content': 'Test Content'}
        orig_log_count = len(models.EmailLog.query.all())
        rv = self.app.post("/api/session/%i/email" % session.id, headers=headers,
                           data=json.dumps(data),  content_type="application/json")
        self.assert_success(rv)

        self.assertGreater(len(TEST_MESSAGES),2)
        self.assertEqual("[edplatform] Test Subject", TEST_MESSAGES[0]['subject'])
        logs = models.EmailLog.query.all()
        self.assertEqual(len(logs), orig_log_count + 3)
        self.assertIsNotNone(logs[0].tracking_code)
        self.assertEqual(logs[0].email_message.subject, data["subject"])
        return session

    def test_get_messages(self):
        session = self.test_email_sends_to_recipient() # Generate some messages.

        rv = self.app.get("/api/session/%i" % session.id, headers=self.logged_in_headers())
        self.assert_success(rv)
        s_result = json.loads(rv.get_data(as_text=True))
        self.assertTrue("messages" in s_result["_links"])

        rv = self.app.get(s_result["_links"]["messages"])
        self.assert_success(rv)
        s_result = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(s_result))

    def test_tracking_logo(self):
        participant = self.get_current_participant()
        email_message = models.EmailMessage()
        email_log = models.EmailLog()
        email_log.participant_id = participant['id']
        email_message.logs.append(email_log)
        db.session.add(email_message)
        db.session.commit()

        self.assertFalse(email_log.opened)
        rv = self.app.get("/api/logo/%i/%s/logo.png" %
                          (participant['id'], email_log.tracking_code))
        self.assert_success(rv)

        updated = models.EmailLog.query.filter_by(tracking_code=email_log.tracking_code).first()
        self.assertTrue(updated.opened)
        self.assertIsNotNone(updated.date_opened)

    def search(self, query):
        self.load_sample_data()
        '''Executes a query, returning the resulting search results object.'''
        rv = self.app.post('/api/workshop/search', data=json.dumps(query), follow_redirects=True,
                           content_type="application/json")
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))


    def test_search_title(self):
        self.load_sample_data()
        data = {'query': 'python', 'filters': []}
        search_results = self.search(data)
        self.assertEqual(7, len(search_results["hits"]))


    def test_search_description(self):
        self.load_sample_data()
        data = {'query': 'amazon web services', 'filters': []}
        search_results = self.search(data)
        self.assertEqual(8, len(search_results["hits"]))
        self.assertEqual("Introduction to Cloud Computing with AWS",
                         search_results["hits"][0]['title'])

    def test_search_location(self):
        self.load_sample_data()
        data = {'query': 'Brown', 'filters': []}
        search_results = self.search(data)
        self.assertEqual(17, search_results["total"])
        self.assertEqual(10, len(search_results["hits"]))
        for w in search_results["hits"]:
            self.assertEqual(w['sessions'][0]['location'],'Brown 133')

    def test_search_instructor(self):
        self.load_sample_data()
        data = {'query': 'Nagraj', 'filters': []}
        search_results = self.search(data)
        self.assertEqual(6, search_results["total"])
        self.assertEqual(6, len(search_results["hits"]))
        for w in search_results["hits"]:
            match = False
            for s in w['sessions']:
                for i in s['instructors']:
                    if(i['display_name'] == 'VP Nagraj (Pete)'): match = True
            assert match, "No matches for Pete in instructors:" + str(w['sessions'][0]['instructors'])

    def test_search_meta(self):
        self.load_sample_data()
        data = {'query': '', 'filters': []}
        results = self.search(data)
        self.assertIn('total', results)
        self.assertEqual(21, results["total"])
        self.assertEqual(10, len(results["hits"]))

    def test_view_instructor_aggregations(self):
        self.load_sample_data()
        data = {'query': '', 'filters': []}
        results = self.search(data)
        self.assertIn('facets', results)
        self.assertIn('instructors', results["facets"])

    def test_filter_on_instructor(self):
        self.load_sample_data()
        data = {'query': '', 'filters': [{'field':'instructors','value':'VP Nagraj (Pete)'}]}
        results = self.search(data)
        self.assertEquals(6, len(results["hits"]))
        self.assertEquals(6, results["total"])
        for hit in results["hits"]:
            match = False
            for session in hit["sessions"]:
                for instructor in session["instructors"]:
                    if(instructor["display_name"] == 'VP Nagraj (Pete)'):
                        match = True
            self.assertTrue(match, "Every hit should now have Pete as an instructor.")

    def test_search_by_date_past(self):
        self.load_sample_data()
        data = {'query': '', 'date_restriction':'past'}
        results = self.search(data)
        for hit in results["hits"]:
            match = False
            for session in hit["sessions"]:
                date = dateutil.parser.parse(session['date_time'])
                present = datetime.datetime.now(datetime.timezone.utc)
                if(date < present): match=True;
            self.assertTrue(match, "Every hit should now have a session in the past.")

    def test_search_by_date_future(self):
        self.load_sample_data()
        data = {'query': '', 'date_restriction':'future'}
        results = self.search(data)
        for hit in results["hits"]:
            match = False
            for session in hit["sessions"]:
                date = dateutil.parser.parse(session['date_time'])
                present = datetime.datetime.now(datetime.timezone.utc)
                if(date >= present): match=True;
            self.assertTrue(match, "Every hit should now have a session in the future.")


if __name__ == '__main__':
    unittest.main()
