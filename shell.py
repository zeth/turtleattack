"""A shell :) for the user to control the game with."""

import threading
import code

class InterpreterThread(threading.Thread):
    """The thread containing the user's interpreter."""
    def __init__(self, world, spider):
        super(InterpreterThread, self).__init__()
        self.world = world
        self.spider = spider

    def run(self):
        code.interact(local={'world': self.world, 'spider': self.spider})
