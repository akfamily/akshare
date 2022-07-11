class ResponseError(Exception):
    """Something was wrong with the response from Google"""

    def __init__(self, message, response):
        super(Exception, self).__init__(message)

        # pass response so it can be handled upstream
        self.response = response
