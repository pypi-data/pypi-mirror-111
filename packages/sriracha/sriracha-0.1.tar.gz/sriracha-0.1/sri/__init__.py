import click
from . import bootstrap
from . import utils

TEMPLATE_REPOSITORY = 'https://github.com/pcranaway/sriracha-template.git'

@click.group()
def main():
    pass

@main.command()
@click.option('--dir',
        default=None,
        callback=utils.validate_directory,
        help='path of the directory that the project should be created in')
@click.argument('name')
def new(dir, name):
    if dir == None:
        dir = name

    bootstrap.new_project(TEMPLATE_REPOSITORY, name, dir)

    print('New project is located at {}'.format(dir))
    utils.write_tty('')
    utils.write_tty('  cd {}'.format(dir))
    utils.write_tty('  bin/dev-start')
    utils.write_tty('')
