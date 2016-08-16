import os


def _find_raw_dir():
    basedir = os.path.dirname(__file__)
    return os.path.join(basedir, 'raw')

RAW_DIR = _find_raw_dir()


def raw_file(name):
    return os.path.join(RAW_DIR, name)
