Turtle Attack - save the world from evil turtle graphics
========================================================

*Turtle attack is a simple computer game that aims to introduce basic programming concepts (via the Python language) without being boring.*

One night after school, we saw strange arrow shapes in the sky. The next morning, very angry turtles began walking out of the sea onto the land - it is a full scale turtle invasion.

The last hope for the world is a friendly spider - help her to catch the evil turtles in her web.

How to run the game
===================

To install the game, use::

    python setup.py install

Then to start the game, use::

    tattack

However, installing using the setup.py file is not required, if you want you can just start the game by typing ./tattack in the source directory.

Gameplay involves using two windows. The game window and the interpreter within your computer's terminal application. You need to size both so they fit comfortably on screen together at once.

Game options
============

When you run the tattack command, you can also provide any (or none) of the following options:

+----+--------------------------------------------------------------+
| -x | Width of the game screen in pixels                           |
+----+--------------------------------------------------------------+
| -y | Height of the game screen in pixels                          |
+----+--------------------------------------------------------------+
| -f | Fullscreen game window (only useful in multi-monitor setups) |
+----+--------------------------------------------------------------+
| -t | Training mode (no enemy turtles)                             |
+----+--------------------------------------------------------------+
| -m | Maximum number of enemy turtles                              |
+----+--------------------------------------------------------------+

Also using -h will show these options, so you do not have to remember them now. So for example, if you want the game screen to be 800 by 800 pixels, and you want to be in training mode, then you need to type::

    tattack -x 800 -y 800 -t

How to end the game
===================

To end the game, close the game window using the close icon (the X in the corner of the window); then leave the interpreter by pressing Ctrl+D (the Control key and the D key at the same time).

If the game does not exit cleanly and it leaves the terminal in an abnormal state (e.g. in the process of customising the game you make TK crash), then use the *reset* command to restore your terminal to its initial state.

The Evil Turtles
----------------

Base Turtle - This is the basic Evil Turtle henchman, he is **green** and not very bright (but useful for basing your own turtles on).

Friendly Turtle - This yellow turtle likes to seek out other **yellow** turtles and form a group.

Ghost Turtle - This **cyan** coloured turtle moves in a straight line but can wraparound the edge of the screen to attack from the other side.

Predator Turtle - This **purple** turtle is a fearless hunter and heads straight for the spider.

Dragon Turtle - When coloured **red**, he breathes fire and burns his way through spider webs. However, eventually he gets tired and turns **orange**, then he is more vulnerable until he gets his breath back.

The Spider
----------

The evil turtles move themselves. You control the spider by typing commands into the interpreter window, the spider responds in the game window.

At the start of the game, there is a starting spider, called somewhat unimaginatively, *spider*. To make the spider move forward 100 pixels, type::

    spider.forward(100)

The spider then moves 100 pixels forward, leaving web as it moves.

To make the spider turn right, type::

    spider.right(90)

Now type again::

    spider.forward(100)

Now the spider has moved again, this time in the new direction.

To make the spider go backwards 100 pixels, use::

    spider.back(100)

To make the spider turn left 90 degrees, use::

    spider.left(100)

To make the spider go back to the centre of the screen use::

    spider.home()

To make the spider go directly to a certain point, use goto, for example, if we want to send the spider to 200 pixels above and 200 pixels right of the starting point, we can use::

    spider.goto(200,200)

As you move around, you make web, the turtles get stuck in the web and become spider food. If you don't eat the spider food, it gets old and disappears.

Watch out for the turtles, if the turtles walk over the spider, she gets squished.

Making a new spider
-------------------
 
If your spider is squished, you will want to make a new one. Also, once you get very good at controlling one spider, you might want to control several.

To have the ability to make new spiders, you have to type this magic spell::

    from turtleattack.spiders import Spider

Now you have the ability to make new spiders in the following way. Firstly,  you need to give a spider a name, then you need to put the spider into the game world. For example, if you wanted to call your spider Sally::

    sally = Spider(world)

Now you can control Sally::

    sally.forward(100)

Lets make another spider called George::

    george = Spider(world)

Now you can control George::

    george.back(100)

Rebuild the home web
--------------------

If you want the ability to automatically rebuild the web at the starting point, you can use the following magic spell:

from turtleattack.spiderweb import Web

Then you need to use the name of a spider and the word Web, so for example, if the starting spider is still alive, you can use::

    Web(spider)

Or if your spider is now called Sally::

    Web(sally)

Advanced Spider control
-----------------------

The spider and the evil turtles are in fact both types of (*subclasses of*) the Python turtle, `this page`_ lists all the available commands (called *methods*) that Python turtles have.

Creating new types of turtles and spiders
-----------------------------------------

To be written.

.. _`this page`: http://docs.python.org/3.3/library/turtle.html#turtle-methods

Tips
----

* Using the up cursor key allows you to access and reuse your command history.

* Try to keep the central home area free of evil turtles so you can create new spiders easily.

* You can chain commands together using semi-colons. For example, you can make the spider leave her safer central zone, lay a square of web and then come back to home, all chained together in one line.

* At the moment there is little balancing for screen size, meaning that a large screen resolution will make it easy on the spider, a small resolution makes it easier for the evil turtles.

* If the game window throws a Python error and freezes, resume it with::

    world.run(-1)

* Learning more Python syntax allows you to automate your spiders in interesting ways. For example, the *for* statement can be a really powerful tool::

    from random import randint
    for i in range(100):
        spider.right(randint(1,360))
        spider.forward(randint(20,300))
