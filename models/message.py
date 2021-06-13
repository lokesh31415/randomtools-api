

class ProcessStatus:
    """
    Different kind of status types to append in the response.
    """
    VALID = 'valid'
    INVALID = 'invalid'
    SUCCESS = 'success'
    ERROR = 'error'
    PROCESS = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

class MessageResponse:
    """
    Model class to use as simple message/error response
    """
    def __init__(self, message: str, status: ProcessStatus=ProcessStatus.VALID, errmsg: str = '') -> None:
        self.status = status
        self.message = message
        self.errmsg = errmsg

    def get_json(self):
        return {'status': self.status, 'message':self.message, 'errorMessage': self.errmsg}