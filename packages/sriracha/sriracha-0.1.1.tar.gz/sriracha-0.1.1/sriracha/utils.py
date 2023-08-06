IGNORE_VARS = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__', '__builtins__']

def handle_request_err(code):
    """
    responds with a handle_request compatible function
    that returns an error code code

    NOTE: shoud we cache this / the lambdas' responses?
    """

    return lambda request: (code, '''
    <!doctype html>
    <html lang="en">
        <head>
            <title>{}</title>
            <meta charset="UTF-8">
        </head>
        <body style="margin: 5%; font-family: Sans-Serif;">
            <h1>{}</h1>
            <p>An error occurred while trying to respond to this request</p>
        </body>
    </html>
    '''.format(code, code))
