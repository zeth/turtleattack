"""Attack of the Turtles"""

from __future__ import division, print_function, absolute_import

from turtleattack.shell import InterpreterThread
from turtleattack.evilworld import EvilTurtleWorld
from turtleattack.spiders import Spider
from turtleattack.spiderweb import Web


def main():
    """Run the main game loop."""
    world = EvilTurtleWorld()
    spider = Spider(world)
    world.turtles.append(spider)
    Web(spider)
    ithread = InterpreterThread(world=world, spider=spider)
    ithread.start()
    world.run(-1)
    print("The game window has stopped.\nPress Ctrl+d to quit.")

if __name__ == '__main__':
    main()
