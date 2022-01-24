from tinydb import TinyDB
import os

os.mkdir("data")
players = TinyDB("data/players.json")
