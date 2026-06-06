from os import getenv

from struture.singleton import Singleton


class Config(Singleton):
    def __init__(self):
        if not self.created:
            self.TOKEN = getenv("TOKEN")
            self.CHANNEL_ID = getenv("CHANNEL_ID")
            self.OWNERS = list(map(int, getenv("OWNERS").split(",")))
