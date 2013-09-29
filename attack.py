"""Attack of the Turtles"""

from __future__ import division, print_function, absolute_import

from shell import InterpreterThread
from evilworld import EvilTurtleWorld
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from spiders import Spider
from borders import border_handler


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
