"""Attack of the Turtle"""

from __future__ import division, print_function, absolute_import

from turtlepower.world import TurtleWorld, PowerTurtle, wrap, clamp, noisy
import time
import queue
import threading
from random import choice, random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SPEED_MODIFIER = 1
BOID_ACCELERATION = 0.1
BOID_ROTATION = 4.0

def remove_at_border(turtle, screen_width, screen_height, world):
    """Remove turtle if it hits the border."""
    x, y = turtle.pos()
    new_x = new_y = None
    if x > screen_width / 2 or x < -screen_width / 2 or \
            y > screen_height / 2 or y < -screen_height / 2:
        world.remove_turtle(turtle)
        world.minions -= 1

def bounce_at_border(turtle, screen_width, screen_height, world):
    """Remove turtle if it hits the border."""
    x, y = turtle.pos()
    new_x = new_y = None
    if x > screen_width / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif x < -screen_width / 2:
        new_heading = turtle.heading() - 180
        if new_heading < 0:
            new_heading = 0
        turtle.setheading(new_heading)
    elif y > screen_height / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif y < -screen_height / 2:
        new_heading = turtle.heading() - 180
        turtle.setheading(new_heading)


class EvilTurtle(PowerTurtle):
    """Evil Killer Turtle."""
    def setup(self):
        """Setup the turtle."""
        self.shape('turtle')
        self.penup()

    def set_position(self):
        """Put the turtle into position."""
        self.world.random_position(self)


class GhostTurtle(EvilTurtle):
    """Basic dumb turtle."""
    def setup(self):
        super(GhostTurtle, self).setup()
        self.fillcolor('cyan')
        self.assigned_speed = random() * 6 * SPEED_MODIFIER

    def callback(self, world):
        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)

class WiddleTurtle(EvilTurtle):
    """Basic dumb turtle."""
    def setup(self):
        super(WiddleTurtle, self).setup()
        self.fillcolor('orange')
        self.clockwise = choice([False, True])
        self.assigned_speed = random() * 4 * SPEED_MODIFIER

    def callback(self, world):
        self.penup()
        self.forward(self.assigned_speed)
        if self.clockwise:
            target_heading = self.heading() - random()*15
        else:
            target_heading = self.heading() + random()*15

        self.turn_towards(target_heading, BOID_ROTATION)
        
        if random() > 0.85:
            if self.clockwise:
                self.clockwise = False
            else:
                self.clockwise = True

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        bounce_at_border(self, screen_width, screen_height, self.world)

class DisappearingTurtle(EvilTurtle):
    """Turtle that has enough and goes home when it hits the side."""
    def setup(self):
        super(DisappearingTurtle, self).setup()
        self.fillcolor('red')
        self.assigned_speed = random() * 1 * SPEED_MODIFIER

    def callback(self, world):
        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        remove_at_border(self, screen_width, screen_height, self.world)

class BouncingTurtle(EvilTurtle):
    """Bouncing dumb turtle."""
    def setup(self):
        super(BouncingTurtle, self).setup()
        self.fillcolor('purple')
        self.assigned_speed = random() * 3 * SPEED_MODIFIER

    def callback(self, world):
        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        bounce_at_border(self, screen_width, screen_height, self.world)

class BoidTurtle(EvilTurtle):

    def setup(self):
        super(BoidTurtle, self).setup()
        self._move = random() * 4
        self.fillcolor('yellow')

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)


    def callback(self, world):
        self.penup()
        neighbours = self.get_neighbours(60, 120)
        if not neighbours:
            self._move = noisy(self._move)
            target_heading = self.heading() + random()*BOID_ROTATION*4 - BOID_ROTATION
        else:
            # cohesion
            center_x = []
            center_y = []
            # alignment
            headings = []
            speeds = []
            # separation
            #close_x = []
            #close_y = []
            myx, myy = self.position()
            for t in neighbours:
                if type(t) == BoidTurtle:
                    x, y = t.position()
                    speeds.append(t._move)
                    headings.append(t.heading)
                    center_x.append(x)
                    center_y.append(y)

            if not speeds or not center_x or not center_y:
                self._move = noisy(self._move)
                target_heading = self.heading() + random()*BOID_ROTATION*2 - BOID_ROTATION
            else:
                target_speed = sum(speeds) / len(speeds)
                delta_speed = min(BOID_ACCELERATION, abs(target_speed - self._move))
                if self._move > target_speed:
                    delta_speed = -delta_speed
                self._move += noisy(delta_speed)

                x1 = sum(center_x) / len(center_x)
                y1 = sum(center_y) / len(center_y)

                target_heading = noisy(self.towards((x1, y1)))

        self.turn_towards(target_heading, BOID_ROTATION)
        self.forward(self._move)

TURTLE_TYPES = [DisappearingTurtle, GhostTurtle, BoidTurtle, \
                    BouncingTurtle, WiddleTurtle]

class BossTurtle(EvilTurtle):
    """Not dumd turtle."""
    pass

class GoodSpider(PowerTurtle):
    """Spider saving the world."""
    pass

class EvilTurtleWorld(TurtleWorld):
    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        super(EvilTurtleWorld, self).__init__(width, height, borders, title)
        self.hatching = 0
        self.minions = 0
        # Start with one
        self.birth_turtle()

    def tick(self):
        super(EvilTurtleWorld, self).tick()
        # Do whatever I want here
        self.hatching += 1
        if self.hatching == 100 / SPEED_MODIFIER:
            self.hatching = 0
            new_turtle = self.birth_turtle()
            
    def birth_turtle(self, turtle_class=None):
        """Put a new turtle into the game."""
        if turtle_class == None:
            turtle_class = choice(TURTLE_TYPES)
        new_turtle = turtle_class(self)
        self.add_turtle(new_turtle)
        new_turtle.set_position()
        self.minions += 1
        print("%s evil turtles" % self.minions)
        return new_turtle



def border_handler(turtle, screen_width, screen_height):
    turtle.handle_border(screen_width, screen_height)

def main():
    """Run the main game loop."""
    world = EvilTurtleWorld(SCREEN_WIDTH, SCREEN_HEIGHT, border_handler, "Attack of the Turtles")
    world.run(-1)
    print("End")

if __name__ == '__main__':
    main()
