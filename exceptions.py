## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AUTH_ERROR(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

class ACTOR_EXCEPTION(Exception):
    pass

class MOVIE_EXCEPTION(Exception):
    pass