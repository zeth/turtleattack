Turtle Attack - putting the violence into Turtle graphics
=========================================================

*Turtle attack is a simple computer game that aims to introduce basic programming concepts (via the Python language) without being boring.*

One night after school, we saw strange arrow shapes in the sky. The next morning, very angry turtles began walking out of the sea onto the land - it is a full scale turtle invasion.

The last hope for the world is a friendly spider - help her to catch the evil turtles in her web.

The Evil Turtles
----------------

Base Turtle - This is the basic Evil Turtle henchman, he is **green** and not very bright (but useful for basing your own turtles on).

Friendly Turtle - This yellow turtle likes to seek out other **yellow** turtles and form a group.

Ghost Turtle - This **cyan** coloured turtle moves in a straight line but can wraparound the edge of the screen.

Predator Turtle - This **purple** turtle is a fearless hunter and heads straight for the spider.

Dragon Turtle - When coloured **red**, he breathes fire and burns his way through spider webs. However, eventually he gets tired and turns **orange**, then he is more vulnerable until he gets his breath back.

The Spider
----------

Gameplay involves using two windows. The game window and the interpreter window. The evil turtles move themselves.

You control the spider by typing commands into the interpreter window, the spider responds in the game window.

At the start of the game, there is a starting spider, called somewhat unimaginatively, *spider*. To make the spider move forward 100 pixels, type::

    spider.forwards(100)

The spider then moves 100 pixels forward, leaving web as it moves.

To make the spider turn right, type::

    spider.right(90)

Now type again::

    spider.forwards(100)

Now the spider has moved again, this time in the new direction.

To make the spider go backwards 100 pixels, use::

    spider.back(100)

To make the spider turn left 90 degrees, use::

    spider.left(100)

To make the spider go back to the centre of the screen use::

    spider.home()

To make the spider go directly to a certain point, use goto, for example, if we want to send the spider to 200 pixels above and 200 pixels right of the starting point, we can use:

    spider.goto(200,200)

As you move around, you make web, the turtles get stuck in the web and become spider food. If you don't eat the spider food, it gets old and disappears.

Watch out for the turtles, if the turtles walk over the spider, she gets squished.

Making a new spider
-------------------
 
If your spider is squished, you will want to make a new one. Also, once you get very good at controlling one spider, you might want to control several.

To have the ability to make new spiders, you have to type this magic spell:

from spiders import Spider

Now you have the ability to make new spiders in the following way. Firstly,  you need to give a spider a name, then you need to put the spider into the game world. For example, if you wanted to call my spider Sally::

    sally = Spider(world)

Now you can control Sally::

    sally.forwards(100)

Lets make another spider called George:

    george = Spider(world)

Now you can contol George:

    george.back(100)

Rebuild the home web
--------------------

If you want the ability to automatically rebuild the web at the starting point, you can use the following magic spell:

from spiderweb import Web

Then you need to use the name of a spider and the word Web, so for example, if the starting spider is still alive, you can use::

    Web(spider)

Or if your spider is now called Sally::

    Web(sally)

Advanced Spider control
-----------------------

The spider and the evil turtles are in fact both types of (*subclasses of*) Python turtles, `this page`_ lists the available commands (called *methods*).

Creating new types of turtles and spiders
-----------------------------------------

To be written.

.. _`this page`: http://docs.python.org/3.3/library/turtle.html#turtle-methods



