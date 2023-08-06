from pathlib import Path


def exists(path_str):
    """
    Method to return True or False whether a resource exists.
    """
    return Path(path_str).exists()
