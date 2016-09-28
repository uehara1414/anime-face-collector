import os


def get_suffix(filename):
    return os.path.splitext(filename)[1]
