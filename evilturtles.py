"""Evil Turtles."""

from random import random, choice
from world import PowerTurtle, wrap, noisy, clamp
from constants import SPEED_MODIFIER, BOID_ACCELERATION, BOID_ROTATION
from borders import bounce_at_border, remove_at_border

class Soup(PowerTurtle):
    """An evil turtle that has been caught in spider web.""" 
    def __init__(self, world, position):
        self.starting_x, self.starting_y = position
        super(Soup, self).__init__(world)
        self.radius = 10
        self.moulding = 0

    def setup(self):
        """Setup the turtle."""
        self.penup()
        self.world.screen.register_shape('soup.gif')
        self.shape('soup.gif')
        self.set_position()

    def set_position(self):
        """Put the soup into position."""
        self.setpos(self.starting_x, self.starting_y)

    def callback(self, world):
        """Check if eaten by spider."""
        self.check_for_spider()
        # Cannot wait forever
        self.moulding += 1
        if self.moulding == 500 / SPEED_MODIFIER:
            self.world.remove_turtle(self)

    def handle_border(self, screen_width, screen_height):
        """Soup doesn't move."""
        clamp(self, screen_width, screen_height)

    def check_for_spider(self):
        """Check if there are any spiders nearby,
        if so, get eaten."""
        for spider in self.world.spiders:
            if self.distance(spider) < self.radius:
                self.eaten()

    def eaten(self):
        """The spider food is eaten."""
        self.write("Yum yum")
        self.world.remove_turtle(self)
        self.world.food_stores += 1

class EvilTurtle(PowerTurtle):
    """Evil Killer Turtle."""

    def __init__(self, world):
        super(EvilTurtle, self).__init__(world)
        self.assigned_speed = 2

    def setup(self):
        """Setup the turtle."""
        self.shape('turtle')
        self.penup()
        self.radius = 10

    def set_position(self):
        """Put the turtle into position."""
        self.world.random_position(self)

    def caught(self):
        """Caught in the web."""
        soup = Soup(self.world, self.pos())
        self.world.turtles.append(soup)
        try:
            self.world.remove_turtle(self)
        except ValueError:
            print ("ValueError:", self)

    def check_for_web(self):
        """Check we are not hitting a web."""
        cur_x, cur_y = self.pos()
        canvas = self.world.screen.cv
        nearby_things = canvas.find_overlapping(
            cur_x - 5,
            cur_y - 5,
            cur_x + 5,
            cur_y + 5)
        for thing_id in nearby_things[:]:
            if canvas.type(thing_id) == 'line':
                # Remove that bit of web
                canvas.delete(thing_id)
                # Turtle is caught
                self.caught()

    def check_for_spider(self):
        """Check if there are any spiders nearby,
        if so, eat them."""
        for spider in self.world.spiders:
            if self.distance(spider) < self.radius:
                spider.die()

    def callback(self, world):
        self.check_for_spider()
        self.check_for_web()
        
    

class GhostTurtle(EvilTurtle):
    """Basic dumb turtle."""
    def setup(self):
        super(GhostTurtle, self).setup()
        self.fillcolor('cyan')
        self.assigned_speed = random() * 6 * SPEED_MODIFIER

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(GhostTurtle, self).callback(world)

        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)


class WiddleTurtle(EvilTurtle):
    """Basic dumb turtle."""
    clockwise = False

    def setup(self):
        super(WiddleTurtle, self).setup()
        self.fillcolor('orange')
        self.clockwise = choice([False, True])
        self.assigned_speed = random() * 4 * SPEED_MODIFIER

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(WiddleTurtle, self).callback(world)
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
        bounce_at_border(self, screen_width, screen_height)


class DisappearingTurtle(EvilTurtle):
    """Turtle that has enough and goes home when it hits the side."""
    def setup(self):
        super(DisappearingTurtle, self).setup()
        self.fillcolor('red')
        self.assigned_speed = random() * 1 * SPEED_MODIFIER

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(DisappearingTurtle, self).callback(world)
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
        """Move the turtle each tick of the game loop."""
        super(BouncingTurtle, self).callback(world)
        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        bounce_at_border(self, screen_width, screen_height)


class BoidTurtle(EvilTurtle):
    """Turtles that form groups."""
    def setup(self):
        super(BoidTurtle, self).setup()
        self._move = random() * 4
        self.fillcolor('yellow')

    def handle_border(self, screen_width, screen_height):
        """Wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(BoidTurtle, self).callback(world)
        self.penup()
        neighbours = self.get_neighbours(60, 120)
        if not neighbours:
            self._move = noisy(self._move)
            target_heading = self.heading() + \
                random() * BOID_ROTATION * 4 - BOID_ROTATION
        else:
            # cohesion
            center_x = []
            center_y = []
            # alignment
            headings = []
            speeds = []
            # separation
            for turt in neighbours:
                if type(turt) == BoidTurtle:
                    old_x, old_y = turt.position()
                    speeds.append(turt._move)
                    headings.append(turt.heading)
                    center_x.append(old_x)
                    center_y.append(old_y)

            if not speeds or not center_x or not center_y:
                self._move = noisy(self._move)
                target_heading = self.heading() + random() * BOID_ROTATION \
                    * 2 - BOID_ROTATION
            else:
                target_speed = sum(speeds) / len(speeds)
                delta_speed = min(BOID_ACCELERATION,
                                  abs(target_speed - self._move))
                if self._move > target_speed:
                    delta_speed = -delta_speed
                self._move += noisy(delta_speed)

                target_x = sum(center_x) / len(center_x)
                target_y = sum(center_y) / len(center_y)

                target_heading = noisy(self.towards((target_x, target_y)))

        self.turn_towards(target_heading, BOID_ROTATION)
        self.forward(self._move)


TURTLE_TYPES = [DisappearingTurtle, GhostTurtle, BoidTurtle,
                BouncingTurtle, WiddleTurtle]
