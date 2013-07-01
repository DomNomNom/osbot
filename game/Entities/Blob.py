import pyglet.gl as gl
import pymunk
from pymunk import Vec2d

from itertools import chain

from Entity import PhysicsEntity


class Blob(PhysicsEntity):

  drawLayer = 'game'
  colour = (1, 0, 0)


  def __init__(self, pos, radius):
    self.pos = pos
    self.radius = radius
    radiusVector = Vec2d(radius, 0)

    self.hitbox = pymunk.Circle(self.body, radius)
    # note: collisionLayers and collisionType get created by physics.py
    self.hitbox.friction = 1
    self.hitbox.layers = Blob.collisionBitmask
    self.hitbox.collision_type = Blob.collisionType
    self.shapes = [self.hitbox]


    self.bodyVerticies = [Vec2d()]
    for i in xrange(0, 365, 5):
      self.bodyVerticies.append(radiusVector.rotated_degrees(i))


  def setupVertexLists(self, batch):
    # vertex lists
    self.vertexLists = [
      batch.add(
        len(self.bodyVerticies),
        gl.GL_TRIANGLE_FAN,
        None, # group
        ('v2f/stream', list(chain(*self.bodyVerticies))),      # verticies
        ('c3f/static', self.colour * len(self.bodyVerticies)), # colour for each vertex (all the same)
      ),
    ]

    # self.lineVertexList = game.engine.drawLayersBatch[self.drawLayer].add(
    #   2,
    #   gl.GL_LINES,
    #   None, # group
    #   ('v2f/stream', list(chain(*[self.pos, self.pos+Vec2d(30, 0).rotated(self.input.currentAim)]))),      # verticies
    #   ('c3f/static', self.lineColour * 2), # colour for each vertex (all the same)
    # )


    def draw():
      self.bodyVertexList.vertices = list(chain(*[v+self.pos for v in self.bodyVerticies]))

      print 'erry frame im renderin'
