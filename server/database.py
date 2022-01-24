import os
from tinydb import TinyDB

os.mkdir("data")
players = TinyDB("data/players.json")
