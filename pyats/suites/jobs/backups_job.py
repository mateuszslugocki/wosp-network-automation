import logging

from pyats.easypy import run


def main():
    logging.root.setLevel("INFO")
    testscript = {
        "testscript": "testscripts/backups.py",
        "datafile": "datafiles/backups.yaml"
    }

    run(**testscript)
