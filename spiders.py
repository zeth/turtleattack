"""Spiders are the heroes of Turtle Attack."""

from random import randrange, randint

from constants import X_OFFSET, Y_OFFSET
from world import PowerTurtle, clamp
from evilturtles import EvilTurtle, PredatorTurtle

class BaseSpider(PowerTurtle):
    """Core spider functions."""
    def __init__(self, world):
        super(BaseSpider, self).__init__(world)

    def callback(self, world):
        pass
    def handle_border(self, screen_width, screen_height):
        return clamp(self, screen_width, screen_height)
    def setup(self):
        super(BaseSpider, self).setup()


class Spider(BaseSpider):
    """Spider saving the world."""

    def __init__(self, world):
        self.clear_insersion_site(world)
        super(Spider, self).__init__(world)

    def clear_insersion_site(self, world):
        """0,0 should be clear of turtles beforehand."""
        for current_turtle in world.turtles:
            if isinstance(current_turtle, EvilTurtle):
                if isinstance(current_turtle, PredatorTurtle):
                    if current_turtle.distance(0,0) < 100:
                        current_turtle.forward(100)
                        current_turtle.freeze()
                else:
                    if current_turtle.distance(0,0) < 30:
                        current_turtle.forward(30)

    def setup(self):
        """Setup the turtle."""
        super(Spider, self).setup()
        self.world.screen.register_shape('spider.gif')
        self.shape('spider.gif')
        self.world.spiders.append(self)
        if self not in self.world.turtles:
            self.world.turtles.append(self)

    def forward(self, distance):
        self.penup()
        self.pendown()
        super(Spider, self).forward(distance)
        self.penup()
        self.pendown()

    def die(self):
        """Remove the spider from the game."""
        self.write("A spider got eaten")
        self.draw_splat()
        self.world.spiders.remove(self)        
        self.world.remove_turtle(self)

    def draw_splat(self):
        """Remains of a spider.
        Spiders do not have red blood but nevermind.
        Could be made a bit curvier.
        
        Idea based on: http://stackoverflow.com/a/10603969
        """
        x, y = self.pos()
        canvas = self.world.screen.cv
        points = [(x + randrange(X_OFFSET), y + randrange(Y_OFFSET))
                  for point in range(randint(10, 30))]
        canvas.create_polygon(points, fill='red', outline='black')
