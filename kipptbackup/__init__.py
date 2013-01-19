"""
Kippt Backup

A simple Python package to allow backup of Kippt clips.
"""

# check if requests exists. couldn't think of a better way to do it.
try:
    import requests
except ImportError:
    pass

if globals().get('requests', None):
    from .backup import KipptBackup

    # we don't really need it
    del requests

__author__ = "Vaidik Kapoor <kapoor.vaidik@gmail.com>"
__license__ = "MIT"
__version__ = ".".join(map(str, (0, 1, 0)))
