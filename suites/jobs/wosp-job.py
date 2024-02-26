import logging

from pyats.easypy import run

def main():
    logging.root.setLevel("INFO")
    testscript = {
            "testscript": "testscripts/wosp-connectivity.py",
        }

    run(**testscript)
