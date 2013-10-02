"""The sea is filled with killer turtles, which are now coming onto land."""

from random import choice, getrandbits

import turtleattack
from turtleattack.evilturtles import BaseTurtle, SPECIAL_TURTLE_TYPES
from turtleattack.constants import SPEED_MODIFIER
from turtleattack.world import TurtleWorld, wrap
import os
from pkgutil import get_loader
import turtleattack
from turtleattack.borders import border_handler
from turtle import TurtleScreen, TK
from tkinter import Tk

    
class EvilTurtleWorld(TurtleWorld):
    """The world window, infected by evil turtles."""
    def __init__(self):
        self.window_title = "Turtle Attack"
        self.borders = border_handler

        args = self.parse_args()
        self.width = args.width
        self.height = args.height
        self.training = args.training
        self.max_turtles = args.max
        self.fullscreen = args.fullscreen

        self.init_screen()

        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.fps = 0
        self.done = True
        self.turtles = []

        #super(EvilTurtleWorld, self).__init__(self.width, self.height, border_handler, "Turtle Attack")
        self.hatching = 0
        self.minions = 0
        self.spiders = []
        self.food_stores = 10
        self.image_location = {}
        self.setup_shapes()
        #print ("Max Width", self.screen.cv.winfo_screenwidth())
        #print ("Max Height", self.screen.cv.winfo_screenheight())

    def parse_args(self):
        """Parse any command line arguments."""
        try:
            from argparse import ArgumentParser
        except ImportError:
            from optparse import OptionParser as ArgumentParser
            ArgumentParser.add_argument = ArgumentParser.add_option
            argparse_available = False
        else:
            argparse_available = True

        parser = ArgumentParser()
        parser.add_argument("-x", "--width", type=int, help="Screen width in pixels")
        parser.add_argument("-y", "--height", type=int, help="Screen height in pixels")
        parser.add_argument("-f", "--fullscreen", default=False, action='store_true',
                            help="Make game window fullscreen, only useful in multi-monitor setups")
        parser.add_argument("-t", "--training", default=False, action='store_true', help="Training mode (no enemy turtles)")
        parser.add_argument("-m", "--max", type=int, default=50, help="Maximum number of enemy turtles (default 50)")
        args = parser.parse_args()
        if not argparse_available:
            args = args[0]
        return args

    def init_screen(self):
        # intialise screen and turn off auto-render
        root = Tk()
        root.wm_title(self.window_title)
        if self.fullscreen:
            self.width = root.winfo_screenwidth()
            self.height = root.winfo_screenheight()
        elif not self.width and not self.height:
            self.width = self.height = min(root.winfo_screenwidth(), root.winfo_screenheight())
        elif not self.width:
            self.width = root.winfo_screenwidth() // 2
        elif not self.height:
            self.height = root.winfo_screenheight()

        window = TK.Canvas(master=root, width=self.width, height=self.height)
        window.pack()
        self.screen = TurtleScreen(window)
        self.screen.tracer(0, 0)

    def tick(self):
        super(EvilTurtleWorld, self).tick()
        if self.spiders:  # No spawning when no player chars
            self.hatching += 1
            if self.hatching == 100 / SPEED_MODIFIER:
                self.hatching = 0
                self.birth_turtle()

    def birth_turtle(self, turtle_class=None):
        """Put a new turtle into the game."""
        if self.training:
            return

        if len(self.turtles) - len(self.spiders) > self.max_turtles:
            # Too many turtles in the game
            return

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
