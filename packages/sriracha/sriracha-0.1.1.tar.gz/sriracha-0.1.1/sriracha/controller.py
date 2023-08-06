class Controller:
    """
    a controller takes care of handling requests on a specific route.

    all classes that extend Controller must have a method called handle_request
    that takes a parameter of type Request and returns either a tuple of an
    integer (response code) and the HTML content, or the HTML content as a
    string in which case the response code defaults to 200 OK
    """

    def __init__(self):
        if not 'handle_request' in dir(self):
            # we create a new handle_request that returns with error code 500
            # and a user-friendly page saying "500"
            self.handle_request = handle_request_err(500)
