"""Constant Values."""

import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SPEED_MODIFIER = 1
BOID_ACCELERATION = 0.1
BOID_ROTATION = 4.0
X_OFFSET = 40
Y_OFFSET = 40
IMAGE_DIR = 'turtleattack/images/'
FIREBALL_IMAGE_NAME = os.path.join(
    IMAGE_DIR, 'fire/fireball-impact-%s.gif')
SPIDER_IMAGE_NAME = os.path.join(IMAGE_DIR, 'spider.gif')
SOUP_IMAGE_NAME = os.path.join(IMAGE_DIR, 'spider.gif')
