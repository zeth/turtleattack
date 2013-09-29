"""Draw a spider web."""
import turtle

CIRCLES = [[(43.30, -25.00), (25.00, -43.30), (0.00, -50.00),
            (-25.00, -43.30), (-43.30, -25.00), (-50.00, -0.00),
            (-43.30, 25.00), (-25.00, 43.30), (-0.00, 50.00),
            (25.00, 43.30), (43.30, 25.00), (50.00, 0.00)],
           [(86.60, -50.00), (50.00, -86.60), (0.00, -100.00),
            (-50.00, -86.60), (-86.60, -50.00), (-100.00, -0.00),
            (-86.60, 50.00), (-50.00, 86.60), (-0.00, 100.00),
            (50.00, 86.60), (86.60, 50.00), (100.00, 0.00)],
           [(129.90, -75.00), (75.00, -129.90), (0.00, -150.00),
            (-75.00, -129.90), (-129.90, -75.00), (-150.00, -0.00),
            (-129.90, 75.00), (-75.00, 129.90), (-0.00, 150.00),
            (75.00, 129.90), (129.90, 75.00), (150.00, 0.00)],
           [(173.21, -100.00), (100.00, -173.21), (0.00, -200.00),
            (-100.00, -173.21), (-173.21, -100.00), (-200.00, -0.00),
            (-173.21, 100.00), (-100.00, 173.21), (-0.00, 200.00),
            (100.00, 173.21), (173.21, 100.00), (200.00, 0.00)]]


class Web(object):
    """A spider web."""
    def __init__(self, spider=None):
        if not spider:
            spider = turtle.Turtle()
        self.spider = spider
        for circle in CIRCLES:
            self.draw_circle(circle)
        self.draw_spokes()

    def draw_spokes(self):
        """Draw the spokes."""
        self.spider.home()
        self.spider.right(30)
        for _ in range(11):
            # draw the spoke
            self.spider.right(30)
            for dummy in range(4):
                self.spider.forward(50)
            # go back to the middle and turn back around
            self.spider.right(180)
            for dummy in range(4):
                self.spider.forward(50)
            self.spider.right(180)

    def draw_circle(self, circle_def):
        """Draw a circle."""
        for point in circle_def:
            self.spider.penup()
            self.spider.pendown()
            self.spider.goto(point)
        self.spider.penup()
        self.spider.pendown()
        self.spider.goto(circle_def[0])


def main():
    """Function for drawing the web on its own."""
    window = turtle.Screen()
    Web()
    window.exitonclick()

if __name__ == '__main__':
    main()
