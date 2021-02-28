"""Shared functions and utilities
"""
import os

from pathlib import Path


def ifnotexistmkdir(directory):
    """If given directory path doesn't exist make it
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
    return Path(directory)
