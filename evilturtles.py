"""Evil Turtles."""

from world import PowerTurtle

class EvilTurtle(PowerTurtle):
    """Evil Killer Turtle."""

    assigned_speed = 2

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
        """Move the turtle each tick of the game loop."""
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

class BossTurtle(EvilTurtle):
    """Not dumd turtle."""
    pass

TURTLE_TYPES = [DisappearingTurtle, GhostTurtle, BoidTurtle,
                BouncingTurtle, WiddleTurtle]
