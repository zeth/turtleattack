"""Functions for dealing with borders."""


def remove_at_border(turtle, screen_width, screen_height, world):
    """Remove turtle if it hits the border."""
    old_x, old_y = turtle.pos()
    if old_x > screen_width / 2 or old_x < -screen_width / 2 or \
            old_y > screen_height / 2 or old_y < -screen_height / 2:
        world.remove_turtle(turtle)
        world.minions -= 1


def bounce_at_border(turtle, screen_width, screen_height):
    """Remove turtle if it hits the border."""
    old_x, old_y = turtle.pos()
    if old_x > screen_width / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif old_x < -screen_width / 2:
        new_heading = turtle.heading() - 180
        if new_heading < 0:
            new_heading = 0
        turtle.setheading(new_heading)
    elif old_y > screen_height / 2:
        new_heading = turtle.heading() + 180
        turtle.setheading(new_heading)
    elif old_y < -screen_height / 2:
        new_heading = turtle.heading() - 180
        turtle.setheading(new_heading)


def border_handler(turtle, screen_width, screen_height):
    """Let each turtle type handle its own border strategy."""
    turtle.handle_border(screen_width, screen_height)
