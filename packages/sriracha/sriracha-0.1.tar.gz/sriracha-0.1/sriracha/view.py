from liquid import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('views/'))
cache = {}

def render_view(name, model):
    """
    renders a view with a model using liquid i think
    """

    # cache the template if it's not already cached
    if not name in cache:
        cache[name] = env.get_template('{}.html'.format(name))

    return cache[name].render(**model)
