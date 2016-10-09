import os


def get_suffix(filename):
    name = os.path.splitext(filename)[1]
    name = name.split('?')[0]
    return name
