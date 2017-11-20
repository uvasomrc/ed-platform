from flask import jsonify


class RestException(Exception):
    status_code = 400
    NOT_FOUND = {'code': 'not_found', 'message': 'Unknown path.'}
    TOKEN_INVALID = {'code': 'token_invalid', 'message': 'Please log in again.'}
    TOKEN_EXPIRED = {'code': 'token_expired', 'message': 'Your session timed out.  Please log in again.'}
    TOKEN_MISSING = {'code': 'token_missing', 'message': 'Your are not logged in.'}
    SESSION_FULL = {'code': 'session_full', 'message': 'This session is full.'}
    NO_SUCH_PARTICIPANT = {'code': 'no_such_participant', 'message': 'This participant does not exist.'}
    NO_SUCH_SESSION = {'code': 'no_such_session', 'message': 'This session does not exist.'}
    NO_SUCH_WORKSHOP = {'code': 'no_such_workshop', 'message': 'This workshop does not exist.'}
    NO_DISCOURSE_TOPIC = {'code': 'no_such_discourse', 'message': 'Discourse ID is missing.'}
    NOT_INSTRUCTOR = {'code': 'not_the_instructor', 'message':'You must be the instructor of this session to perform this action.'}
    ELASTIC_ERROR = {'code': 'elastic_error', 'message':"Error connecting to ElasticSearch."}
    NO_SUCH_CODE = {'code': 'no_such_code', 'message': 'This Track Code does not exist, and cannot be assigned.'}
    NOT_YOUR_ACCOUNT = {'code': 'permission_denied', 'message': 'You may not edit another users account.'}
    PERMISSON_DENIED = {'code': 'permission_denied', 'message': 'You are not authorized to make this call.'}

    def __init__(self, payload, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload)
        return rv