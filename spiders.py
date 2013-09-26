"""Spiders are the heroes of Turtle Attack."""

from world import PowerTurtle

class BaseSpider(PowerTurtle):
    """Core spider functions."""
    def callback(self, world):
        pass
    def handle_border(self, screen_width, screen_height):
        return clamp(self, screen_width, screen_height)


class Spider(BaseSpider):
    """Spider saving the world."""
    pass
