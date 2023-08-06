from types import ModuleType
from . import utils
from .request import Request
import re

class Application:
    """
    an application is an application.

    note: only one application can be created per runtime! (this is not very
    strict, i'm not gonna tell your parents, it's just gonna fuck up)
    """

    def __init__(self, settings_module: ModuleType):
        # hacky way to get all variables that are not weird python variables
        self.settings = {key: value for key, value in vars(settings_module).items() if not key in utils.IGNORE_VARS}

        if not 'routes' in self.settings:
            raise Exception('there are no routes')

        self.routes = self.settings['routes']

    def find_controller_by_path(self, path):
        """
        finds a controller by a path (and returns it).

        routes are defined on the routes variable on the settings, paths are
        are ~~specified using regex~~ matched using == for now
        """

        for rpath, controller in self.routes.items():
            if rpath.lower() == path.lower():
                return controller
        

    def __call__(self, environ, start_response):
        """
        per WSGI, this method is called on every request

        TODO: clean up
        """

        request = Request(environ)
        controller = self.find_controller_by_path(request.path)

        if controller == None:
            start_response('404', [('Content-Type', 'text/html')])
            return [utils.handle_request_err(404)(request)[1].encode()]

        # handle the request
        response = controller.handle_request(request)

        # get status code and content from response
        status = ''
        content = ''

        if type(response) == tuple:
            content = response[1]

            if type(response[0]) == int:
                status = str(response[0])
        else:
            content = response
            status = '200 OK'

        # get response headers
        headers = request.response_headers

        # make this: check if there's already a conte-ttype header, depend on
        # the actual content we're returning 
        headers.append(('Content-Type', 'text/html'))

        # get new cookies
        for cookie, value in request.response_cookies.items():
            headers.append(('Set-Cookie', '{}={}'.format(cookie, value)))

        # respond
        start_response(status, headers)

        return [content.encode()]
