from . import utils
import os
from git import Repo

def new_project(template, name, path):
    """
    creates a new project from a template

    the process goes as:
        - make sure that the parent directory of $path exists (the `new`
          command already does this, but we need to verify it here in case this
          is called from somewhere else that doesn't check that)
        - create new directory on $path if nonexistent
        - clone $template inside that directory
        - replace project_name variable inside every file (wish i could use
          sed on this but apparently it has to be "cross-platform")
    
    """

    # basically replace the exception with a generic Exception if raised
    validated = None
    try:
        validated = utils.validate_directory(None, None, path)
    except Exception:
        pass

    if validated == None:
        raise Exception('parent directory of the project is nonexistent or a file')

    # create directory of project
    os.mkdir(path)

    # clone template
    Repo.clone_from(template, path)

    # replace $project_name$
    # for root, dirs, files in os.walk(path):
    #     for fp in files:
    #         with open(os.path.join(root, fp), 'r+') as file:
    #             for line in file.readlines():
    #                 file.write(line.replace('$project_name$', name))
