"""The sea is filled with killer turtles, which are now coming onto land."""

from random import choice, getrandbits

import turtleattack
from turtleattack.evilturtles import BaseTurtle, SPECIAL_TURTLE_TYPES
from turtleattack.constants import SPEED_MODIFIER
from turtleattack.world import TurtleWorld, wrap
import os
from pkgutil import get_loader
import turtleattack


class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0
        self.spiders = []
        self.food_stores = 10
        self.max_turtles = 50
        self.image_location = {}
        self.setup_shapes()


    def tick(self):
        super(EvilTurtleWorld, self).tick()
        if self.spiders:  # No spawning when no player chars
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
            if getrandbits(1):
                turtle_class = choice(SPECIAL_TURTLE_TYPES)
            else:
                turtle_class = BaseTurtle

        new_turtle = turtle_class(self)
        self.add_turtle(new_turtle)
        new_turtle.set_position()
        self.minions += 1
        return new_turtle

    def setup_shapes(self):
        """Load the shapes."""
        self.load_shape('spider')
        self.load_shape('soup')
        for num in range(1,17):
            self.load_shape('fireball-impact-%s' % num)

    def load_shape(self, shape_name):
        """Find shape location and register it."""
        # Work out the path
        long_path = self.get_resource_location('images/%s.gif' % shape_name)
        # Register the path
        self.screen.register_shape(long_path)
        # Store the path for further use
        self.image_location[shape_name] = long_path

    def get_resource_location(self, resource):
        """Get location of the resource."""
        loader = get_loader(turtleattack)
        parts = resource.split('/')
        parts.insert(0, os.path.dirname(loader.get_filename()))
        resource_name = os.path.join(*parts)
        if os.path.exists(resource_name):
            return resource_name
        # Try to find the image otherwise
        if os.path.exists(resource):
            return resource
        else:
            raise RuntimeError("Cannot find image location.")
