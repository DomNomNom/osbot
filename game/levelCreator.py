import random

import pymunk
from pymunk import Vec2d

import controllers

# Entities
from Entities.Blob import Blob
from Entities.Wall import Wall


# screen sizes. TODO: get these from the engine somehow
wd = 640
ht = 480

allControllers = controllers.allControllers.values()

def randomizeCircle(circle):
    radius = 20 + random.random()*10
    circle.unsafe_set_radius(radius)
    circle.unsafe_set_offset((
        random.random() * (wd-2*radius) + radius,
        random.random() * (ht-2*radius) + radius,
    ))

# procedurally creates a level.
def createLevel(levelName):

    entities = [
        # a box around the screen
        Wall( (-10, 300), ( 10, 300) ),
        Wall( (650, 300), ( 10, 300) ),
        Wall( (300, -10), (400,  10) ),
        Wall( (300, 490), (400,  10) ),
    ]

    # create blobs such that they don't intersect
    space = pymunk.Space()
    for i in xrange(20):
        hitTest = pymunk.Circle(space.static_body, 1, Vec2d(-1, -1))
        randomizeCircle(hitTest)

        collisions = 1000 # how often we query for new positions before saying "no more space left"
        while collisions and space.shape_query(hitTest):
            randomizeCircle(hitTest)
            collisions -= 1

        if not collisions:
            print "no more space left when creating a level. stopping level creation"
            break

        velocity = Vec2d(random.random() * 100, 0)
        velocity.rotate_degrees(random.random() * 360)

        space.add(hitTest)
        entities.append(Blob(
            random.choice(allControllers),
            hitTest.offset,
            hitTest.radius,
            vel=velocity,
        ))

    return entities
