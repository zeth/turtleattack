"""The sea is filled with killer turtles, which are now coming onto land."""

from random import choice, getrandbits

from evilturtles import BaseTurtle, SPECIAL_TURTLE_TYPES
from constants import SPEED_MODIFIER, FIREBALL_IMAGE_NAME
from world import TurtleWorld, wrap


class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0
        self.spiders = []
        self.food_stores = 10
        self.max_turtles = 50
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
        #print("%s evil turtles" % self.minions)
        return new_turtle

    def setup_shapes(self):
        """Load the shapes."""
        self.screen.register_shape('spider.gif')
        self.screen.register_shape('soup.gif')
        for num in range(1,17):
            self.screen.register_shape(FIREBALL_IMAGE_NAME % num)

