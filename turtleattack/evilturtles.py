"""Evil Turtles."""

from random import random, choice, randint
from turtleattack.world import PowerTurtle, wrap, noisy, clamp
from turtleattack.constants import (SPEED_MODIFIER, BOID_ACCELERATION,
                       BOID_ROTATION, SCREEN_WIDTH)
from turtleattack.borders import bounce_at_border, remove_at_border


class Fireball(PowerTurtle):
    """Dangerous fire made by the DragonTurtle."""
    def __init__(self, world, position):
        self.starting_x, self.starting_y = position
        self.fire_count = 1
        self.fire_tick = 1
        super(Fireball, self).__init__(world)

    def update_fire(self):
        """Update the image."""
        self.fire_count += 1
        if self.fire_count == 17:
            self.world.remove_turtle(self)
        elif self.fire_count < 17:
            self.shape(self.world.image_location['fireball-impact-%s' % self.fire_count])

    def set_position(self):
        """Put the fireball into position."""
        self.setpos(self.starting_x, self.starting_y)

    def setup(self):
        """Setup the fireball."""
        self.penup()
        self.shape(self.world.image_location['fireball-impact-1'])
        self.set_position()
        self.check_for_web()
        
    def callback(self, world):
        """Fade to nothing, and kill any passing spiders."""
        self.fire_tick += 1
        if self.fire_tick >= 5 / SPEED_MODIFIER:
            self.fire_tick = 1
            self.update_fire()

    def handle_border(self, screen_width, screen_height):
        """Fireball doesn't move."""
        clamp(self, screen_width, screen_height)

    def check_for_web(self):
        """Burn any nearby web."""
        cur_x, cur_y = self.pos()
        canvas = self.world.screen.cv
        nearby_things = canvas.find_overlapping(
            cur_x - 10,
            cur_y - 10,
            cur_x + 10,
            cur_y + 10)
        for thing_id in nearby_things[:]:
            if canvas.type(thing_id) == 'line':
                # Remove that bit of web
                canvas.delete(thing_id)


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
        self.shape(self.world.image_location['soup'])
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


class BaseTurtle(PowerTurtle):
    """Evil Killer Turtle.
    This is the base EvilTurtle henchman, not very bright.
    """

    def __init__(self, world):
        super(BaseTurtle, self).__init__(world)
        self.frozen = False
        self.freeze_count = 0
        self.truecolor = None
        self.radius = 10
        self.clockwise = choice([False, True])

    def setup(self):
        """Setup the turtle."""
        self.shape('turtle')
        self.penup()
        self.assigned_speed = random() * 4 * SPEED_MODIFIER
        self.fillcolor('green')

    def get_random_pos(self):
        """Get a random pos which is not in the home zone."""
        pos = (randint(-self.world.half_width, self.world.half_width),
               randint(-self.world.half_height, self.world.half_height))
        if pos[0] < 200 and pos[0] > -200 and pos[1] < 200 and pos[1] > -200:            # We are in the home zone, roll again
            return self.get_random_pos()
        else:
            return pos

    def set_position(self, pos=None, angle=None):
        # move to location
        self.hideturtle()
        self.penup()
        if pos is None:
            pos = self.get_random_pos()
        x, y = pos
        self.goto(x, y)
        if angle is None:
            angle = random() * 360
        self.setheading(angle)
        # ready to go
        self.showturtle()
        self.pendown()

    #def set_position(self):
    #    """Put the turtle into position."""
    #    self.world.random_position(self)

    def caught(self):
        """Caught in the web."""
        soup = Soup(self.world, self.pos())
        self.world.turtles.append(soup)
        try:
            self.world.remove_turtle(self)
        except ValueError:
            # Already gone, not sure why?
            pass

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

    def pre_callback(self):
        if self.frozen:
            self.thaw()
        else:
            self.check_for_spider()
            self.check_for_web()

    def freeze(self):
        """Freeze the turtle for a bit."""
        self.frozen = True
        self.truecolor = self.fillcolor()
        self.fillcolor('white')
        self.freeze_count = 300 / SPEED_MODIFIER

    def thaw(self):
        """Melt the turtle a bit."""
        self.freeze_count -= 1
        if self.freeze_count == 0:
            self.fillcolor(self.truecolor)
            self.frozen = False

    def handle_border(self, screen_width, screen_height):
        """Just turn around at the border."""
        bounce_at_border(self, screen_width, screen_height)

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        self.pre_callback()
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


class GhostTurtle(BaseTurtle):
    """Goes in a straight line, but can wrap like a Pac-Man ghost."""
    def setup(self):
        super(GhostTurtle, self).setup()
        self.fillcolor('cyan')
        self.assigned_speed = random() * 6 * SPEED_MODIFIER

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(GhostTurtle, self).pre_callback()
        self.penup()
        self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Ghost turtles wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)


class DragonTurtle(BaseTurtle):
    """The Dragon Turtle leaves a trail of fire and is not affected by web,
    however it can get tired out and then is vulnerable."""

    def setup(self):
        super(DragonTurtle, self).setup()
        self.fillcolor('red')
        self.assigned_speed = random() * 1 * SPEED_MODIFIER
        self.live_fire = True 
        self.charge = SCREEN_WIDTH * 3
        self.recharge = 0

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(DragonTurtle, self).pre_callback()
        self.penup()
        if self.live_fire:
            self.turn_sometimes()
            self.forward(self.assigned_speed)
            self.charge -= self.assigned_speed
            if self.charge < 0:
                self.out_of_battery()
        else:
            self.forward(self.assigned_speed / 3)
            self.recharge -= self.assigned_speed
            if self.recharge < 0:
                self.recharged()

    def out_of_battery(self):
        """Give the DragonTurtle a rest."""
        self.fillcolor('orange')
        self.live_fire = False
        self.recharge = SCREEN_WIDTH

    def recharged(self):
        """All rested, get the fire back out."""
        self.fillcolor('red')
        self.live_fire = True
        self.charge = SCREEN_WIDTH * 3

    def handle_border(self, screen_width, screen_height):
        """Bounce at the border."""
        bounce_at_border(self, screen_width, screen_height)

    def caught(self):
        """DragonTurtle breaks through the web with fire."""
        if self.live_fire:
            fireball = Fireball(self.world, self.pos())
            self.world.turtles.append(fireball)
        else:
            super(DragonTurtle, self).caught()

    def turn_sometimes(self):
        """Move the turte around sometimes."""
        roll = randint(1,50)
        if roll < 5:
            target_heading = self.heading() - random()*15
        elif roll > 45:
            target_heading = self.heading() + random()*15
        elif roll == 25:
            if self.world.spiders:
                target_heading = self.towards(0,0)
            else:
                return
        elif roll == 35:
            spider_distances = {
                self.distance(spider): spider for spider in
                self.world.spiders[:]}
            try:
                target = spider_distances[min(spider_distances)]
            except ValueError:
                # I.e. no spider on screen at the moment
                # Just relax
                return
            target_heading = self.towards(target)
        else:
            return
        self.turn_towards(target_heading, 360)


class FriendlyTurtle(BaseTurtle):
    """Turtles that form groups."""
    def setup(self):
        super(FriendlyTurtle, self).setup()
        self._move = random() * 4
        self.fillcolor('yellow')

    def handle_border(self, screen_width, screen_height):
        """Wrap like in Pac-Man."""
        wrap(self, screen_width, screen_height)

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(FriendlyTurtle, self).pre_callback()
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
                if type(turt) == FriendlyTurtle:
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


class PredatorTurtle(BaseTurtle):
    """Turtle that hunts spiders."""

    def setup(self):
        super(PredatorTurtle, self).setup()
        self.fillcolor('purple')
        self.assigned_speed = random() * 7 * SPEED_MODIFIER

    def callback(self, world):
        """Move the turtle each tick of the game loop."""
        super(PredatorTurtle, self).pre_callback()
        self.penup()
        if not self.frozen:
            self.hunt()

    def hunt(self):
        """Find the closest spider."""
        spider_distances = {
            self.distance(spider): spider for spider in
            self.world.spiders[:]}
        try:
            target = spider_distances[min(spider_distances)]
        except ValueError:
            # I.e. no spider on screen at the moment
            # Just relax
            self.forward(self.assigned_speed / 2)
        else:
            self.turn_towards(self.towards(target), 360)
            self.forward(self.assigned_speed)

    def handle_border(self, screen_width, screen_height):
        """Bounce at the border."""
        bounce_at_border(self, screen_width, screen_height)


SPECIAL_TURTLE_TYPES = [DragonTurtle, GhostTurtle, FriendlyTurtle,
                        PredatorTurtle]
