import os.path
from click import BadParameter

def validate_directory(ctx, param, value):
    """
    validates that the parent directory of a path exists.

    this is used as a callback by click, so it doesn't return a bool, instead,
    it returns the value if validated, and raises a click.BadParameter
    exception if not.
    """
    # this is None in the case that the user has't specified a different
    # directory for their project, so we just return None and pray click won't
    # have a problem with that
    if value == None:
        return None

    # os.path.split, believe it or not, splits a path into two parts, the one
    # being everything before the last slash, and the second being the part
    # after the slash, so the final directory/file. we obviously need the first
    # path to verify that it exists, so we can create the second path.
    if os.path.split(value)[0] == '':
        return value

    parent = os.path.split(value)[0]

    if not os.path.exists(parent):
        raise BadParameter('parent directory does not exist')

    if not os.path.isdir(parent):
        raise BadParameter('parent directory is not a directory')

    return value

def write_tty(content):
    """
    writes to /dev/tty, which redirects to the actual current tty. this helps
    us bypass redirected output and lets us print our soydev messages without
    affecting the actual output of the program
    """

    # there SHOULD be a better way to do it, come on!
    with open('/dev/tty', 'w') as tty:
        tty.write('{}\n'.format(content))
