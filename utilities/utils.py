import os


def get_project_root():
    """returns the root path to the project. Accessing files within project root should be done with the built in
    os.path.join() function and including this functions return as the first parameter. This will allow cross platform
    execution"""

    return os.path.dirname(os.path.abspath(__file__)).strip('utilities')