import os
from tinydb import TinyDB

try:
    os.mkdir("data")
# pylint: disable=broad-except
except Exception:
    pass
players = TinyDB("data/players.json")
