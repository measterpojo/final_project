

from .messages import ExceptionError





class BadRequest(Exception):
    status_code = 400
    default_detail = ExceptionError.BAD_REQUEST

    def __init__(self, detail=None, status_code = None):
        if status_code:
            self.status_code = status_code
        if not detail:
            detail = self.default_detail
        self.detail = detail
    