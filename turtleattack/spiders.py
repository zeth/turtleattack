"""Spiders are the heroes of Turtle Attack."""

from random import randrange, randint

from constants import X_OFFSET, Y_OFFSET
from world import PowerTurtle, clamp
from evilturtles import BaseTurtle, PredatorTurtle

from spiderdecorators import (reuse_doc, living_required,
                              individualise_lines)


class Spider(PowerTurtle):
    """Spider saving the world."""

    def __init__(self, world):
        self.clear_insersion_site(world)
        super(Spider, self).__init__(world)
        self.squished = False

    @staticmethod
    def clear_insersion_site(world):
        """0,0 should be clear of turtles beforehand."""
        for current_turtle in world.turtles:
            if isinstance(current_turtle, BaseTurtle):
                if isinstance(current_turtle, PredatorTurtle):
                    if current_turtle.distance(0, 0) < 100:
                        current_turtle.forward(100)
                        current_turtle.freeze()
                else:
                    if current_turtle.distance(0, 0) < 30:
                        current_turtle.forward(30)

    def setup(self):
        """Setup the turtle."""
        super(Spider, self).setup()
        self.world.screen.register_shape('spider.gif')
        self.shape('spider.gif')
        self.world.spiders.append(self)
        if self not in self.world.turtles:
            self.world.turtles.append(self)

    def die(self):
        """Remove the spider from the game."""
        self.penup()
        self.write("A spider got eaten")
        self.draw_splat()
        self.world.spiders.remove(self)
        self.world.remove_turtle(self)
        self.squished = True

    def draw_splat(self):
        """Remains of a spider.
        Spiders do not have red blood but nevermind.
        Could be made a bit curvier.

        Idea based on: http://stackoverflow.com/a/10603969
        """
        xcoord, ycoord = self.pos()
        canvas = self.world.screen.cv
        points = [(xcoord + randrange(X_OFFSET), ycoord + randrange(Y_OFFSET))
                  for point in range(randint(10, 30))]
        canvas.create_polygon(points, fill='red', outline='black')

    def callback(self, world):
        """Action upon tick."""
        pass

    def handle_border(self, screen_width, screen_height):
        """Don't go outside the borders of the screen."""
        return clamp(self, screen_width, screen_height)

    @reuse_doc(PowerTurtle.forward)
    @living_required
    @individualise_lines
    def forward(self, distance):
        """Make the spider go forward."""
        super(Spider, self).forward(distance)

    @reuse_doc(PowerTurtle.back)
    @living_required
    @individualise_lines
    def back(self, distance):
        super(Spider, self).backward(distance)

    @reuse_doc(PowerTurtle.right)
    @living_required
    def right(self, angle):
        super(Spider, self).right(angle)

    @reuse_doc(PowerTurtle.left)
    @living_required
    def left(self, angle):
        super(Spider, self).left(angle)

    @reuse_doc(PowerTurtle.goto)
    @living_required
    def goto(self, x, y=None):
        super(Spider, self).goto(x, y)

    @reuse_doc(PowerTurtle.setx)
    @living_required
    def setx(self, x):
        super(Spider, self).setx(x)

    @reuse_doc(PowerTurtle.sety)
    @living_required
    def sety(self, y):
        super(Spider, self).sety(y)

    @reuse_doc(PowerTurtle.setheading)
    @living_required
    def setheading(self, to_angle):
        super(Spider, self).setheading(to_angle)

    @reuse_doc(PowerTurtle.home)
    @living_required
    def home(self):
        super(Spider, self).home()

    @reuse_doc(PowerTurtle.circle)
    @living_required
    def circle(self, radius, extent=None, steps=None):
        super(Spider, self).circle(radius, extent, steps)

    @reuse_doc(PowerTurtle.dot)
    @living_required
    def dot(self, size=None, *color):
        super(Spider, self).dot(size, *color)

    @reuse_doc(PowerTurtle.stamp)
    @living_required
    def stamp(self):
        super(Spider, self).stamp()

    @reuse_doc(PowerTurtle.undo)
    @living_required
    def undo(self):
        super(Spider, self).undo()

    @reuse_doc(PowerTurtle.speed)
    @living_required
    def speed(self, speed=None):
        super(Spider, self).speed(speed)

    fd = forward
    bk = back
    backward = back
    rt = right
    lt = left
    setpos = goto
    setposition = goto
    seth = setheading
