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


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SPEED_MODIFIER = 1
BOID_ACCELERATION = 0.1
BOID_ROTATION = 4.0

class InterpreterThread(threading.Thread):
    def __init__(self, world):
        super(InterpreterThread, self).__init__()
        self.world = world

    def run(self):
        print ("Hello from thread")
        WORLD = self.world
        code.interact(local=locals())


def remove_at_border(turtle, screen_width, screen_height, world):
    """Remove turtle if it hits the border."""
    old_x, old_y = turtle.pos()
    if old_x > screen_width / 2 or old_x < -screen_width / 2 or \
            old_y > screen_height / 2 or old_y < -screen_height / 2:
        world.remove_turtle(turtle)
        world.minions -= 1


def bounce_at_border(turtle, screen_width, screen_height):
    """Remove turtle if it hits the border."""
    old_x, old_y = turtle.pos()
    if old_x > screen_width / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif old_x < -screen_width / 2:
        new_heading = turtle.heading() - 180
        if new_heading < 0:
            new_heading = 0
        turtle.setheading(new_heading)
    elif old_y > screen_height / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif old_y < -screen_height / 2:
        new_heading = turtle.heading() - 180
        turtle.setheading(new_heading)


class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0
        # Start with one
        #self.birth_turtle()

    def tick(self):
        super(EvilTurtleWorld, self).tick()
        # Do whatever I want here
        self.hatching += 1
        if self.hatching == 100 / SPEED_MODIFIER:
            self.hatching = 0
            #self.birth_turtle()

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


def border_handler(turtle, screen_width, screen_height):
    """Let each turtle type handle its own border strategy."""
    turtle.handle_border(screen_width, screen_height)


def main():
    """Run the main game loop."""
    world = EvilTurtleWorld(
        SCREEN_WIDTH, SCREEN_HEIGHT,
        border_handler, "Attack of the Turtles")
    t = InterpreterThread(world=world)
    t.start()
    world.run(-1)
    print("End")

if __name__ == '__main__':
    main()
