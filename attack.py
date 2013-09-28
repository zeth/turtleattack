"""Attack of the Turtles"""

from __future__ import division, print_function, absolute_import

import threading
from random import choice
import code

from world import TurtleWorld, wrap
from spiders import Spider
from evilturtles import TURTLE_TYPES
from constants import SPEED_MODIFIER, SCREEN_WIDTH, SCREEN_HEIGHT
from borders import border_handler


class InterpreterThread(threading.Thread):
    """The thread containing the user's interpreter."""
    def __init__(self, world, spider):
        super(InterpreterThread, self).__init__()
        self.world = world
        self.spider = spider

    def run(self):
        code.interact(local={'world': self.world, 'spider': self.spider})


class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0
        self.spiders = []
        self.food_stores = 10
        self.max_turtles = 50

    def tick(self):
        super(EvilTurtleWorld, self).tick()
        # Do whatever I want here
        self.hatching += 1
        if self.hatching == 100 / SPEED_MODIFIER:
            self.hatching = 0
            self.birth_turtle()

    def birth_turtle(self, turtle_class=None):
        """Put a new turtle into the game."""
        if len(self.turtles) - len(self.spiders) > self.max_turtles:
            # Too many turtles in the game
            return None

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
    ithread = InterpreterThread(world=world, spider=spider)
    ithread.start()
    world.run(-1)
    print("The game window has stopped.\nPress Ctrl+d to quit.")

if __name__ == '__main__':
    main()
