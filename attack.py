"""Attack of the Turtles"""

from __future__ import division, print_function, absolute_import

import time
import queue
import threading
from random import choice, random
import code

from world import TurtleWorld, PowerTurtle, wrap, clamp, noisy
from spiders import Spider
from evilturtles import DisappearingTurtle, GhostTurtle, \
    BoidTurtle, BouncingTurtle, WiddleTurtle, TURTLE_TYPES
from constants import *
from borders import border_handler


class InterpreterThread(threading.Thread):
    def __init__(self, world, spider):
        super(InterpreterThread, self).__init__()
        self.world = world
        self.spider = spider

    def run(self):
        WORLD = self.world
        spider = self.spider
        code.interact(local=locals())


class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0

    def tick(self):
        super(EvilTurtleWorld, self).tick()
        # Do whatever I want here
        self.hatching += 1
        if self.hatching == 100 / SPEED_MODIFIER:
            self.hatching = 0
            self.birth_turtle()

    def birth_turtle(self, turtle_class=None):
        """Put a new turtle into the game."""
        if not turtle_class:
            turtle_class = choice(TURTLE_TYPES)
        new_turtle = turtle_class(self)
        self.add_turtle(new_turtle)
        new_turtle.set_position()
        self.minions += 1
        #print("%s evil turtles" % self.minions)
        return new_turtle


def main():
    """Run the main game loop."""
    world = EvilTurtleWorld(
        SCREEN_WIDTH, SCREEN_HEIGHT,
        border_handler, "Attack of the Turtles")
    spider = Spider(world)
    world.turtles.append(spider)
    t = InterpreterThread(world=world, spider=spider)
    t.start()
    world.run(-1)
    print("End")

if __name__ == '__main__':
    main()
