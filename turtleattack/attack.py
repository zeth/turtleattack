"""Attack of the Turtles"""

from __future__ import division, print_function, absolute_import

from turtleattack.shell import InterpreterThread
from turtleattack.evilworld import EvilTurtleWorld
from turtleattack.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from turtleattack.spiders import Spider
from turtleattack.borders import border_handler
from turtleattack.spiderweb import Web

def main():
    """Run the main game loop."""
    world = EvilTurtleWorld(
        SCREEN_WIDTH, SCREEN_HEIGHT,
        border_handler, "Attack of the Turtles")
    spider = Spider(world)
    world.turtles.append(spider)
    Web(spider)
    ithread = InterpreterThread(world=world, spider=spider)
    ithread.start()
    world.run(-1)
    print("The game window has stopped.\nPress Ctrl+d to quit.")

if __name__ == '__main__':
    main()
