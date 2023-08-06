class Request:
    """
    A request is sadly a class (we might take a different approach to this
    later, perhaps a dict) that represents a HTTP request.
    """

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.query_string = environ['QUERY_STRING']

        # apparently dict comprehasions exist!  i noticed on gunicorn
        # (hopefully same on all servers) that all headers are prefixed with
        # HTTP_ on environ
        self.headers = { key.split('HTTP_')[1] : value for key, value in environ.items() if 'HTTP_' in key }

        self.address = (environ['REMOTE_ADDR'], environ['REMOTE_PORT'])
        self.path = environ['PATH_INFO']
   
        # please work
        if 'COOKIE' in self.headers:
            # self.cookies = [tuple(cookie.split('=')) for cookie in self.headers['COOKIE'].split('; ')]

            self.cookies = {cookie.split('=')[0] : cookie.split('=')[1] for cookie in self.headers['COOKIE'].split('; ')}
        else:
            self.cookies = {}

        self.response_headers = []
        self.response_cookies = {}

    def header(self, header, value):
        """
        sets a response header 
        """

        self.response_headers.append((header, value))

    def cookie(self, cookie, value):
        """
        sets a cookie
        """

        self.response_cookies[cookie] = value
        self.cookies[cookie] = value
