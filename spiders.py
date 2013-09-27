"""Spiders are the heroes of Turtle Attack."""

from world import PowerTurtle, clamp

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
        super(Spider, self).__init__(world)

    def setup(self):
        """Setup the turtle."""
        super(Spider, self).setup()
        self.world.screen.register_shape('spider.gif')
        self.shape('spider.gif')
        #self.world.turtles.append(self)
