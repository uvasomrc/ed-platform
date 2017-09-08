from flask import jsonify


class RestException(Exception):
    status_code = 400
    TOKEN_INVALID = {'code': 'token_invalid', 'message': 'Please log in again.'}
    TOKEN_EXPIRED = {'code': 'token_expired', 'message': 'Your session timed out.  Please log in again.'}
    TOKEN_MISSING = {'code': 'token_missing', 'message': 'Your are not logged in.'}

    def __init__(self, payload, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload)
        return rv