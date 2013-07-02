import pyglet.gl as gl
import pymunk
from pymunk import Vec2d


from itertools import chain
from math import pi

from Entity import PhysicsEntity
from  game.Camera import shiftView

class Blob(PhysicsEntity):

  drawLayer = 'game'

  colour = (1, 0, 0)


  def radius_get(self):  return self._radius
  def radius_set(self, radius):
    assert radius > 0
    self._radius = radius
    self.hitbox.unsafe_set_radius(radius)
    self.body.mass = pi * radius**2
    self.radiusVector = Vec2d(radius, 0)
    self.bodyVerticies = [Vec2d()] # recalculate verticies (this could be done with a matrix transform)
    for i in xrange(0, 365, 5):
      self.bodyVerticies.append(self.radiusVector.rotated_degrees(i))
  radius = property(radius_get, radius_set)



  def __init__(self, pos, radius, vel=None):
    self.body = pymunk.Body(mass=pi*radius**2, moment=float('inf'))
    self.body.position = Vec2d(pos)
    self.body.velocity = Vec2d(vel)
    self.hitbox = pymunk.Circle(self.body, radius)
    self.hitbox.layers = Blob.collisionBitmask
    self.hitbox.collision_type = Blob.collisionType
    self.shapes = [self.hitbox]

    self.radius = radius # note: calls setter
    self.id = id(self)


  # def setupVertexLists(self, batch):
    # vertex lists
    # self.bodyVertexList = batch.add(
    #   len(self.bodyVerticies),
    #   gl.GL_TRIANGLE_FAN,
    #   None, # group
    #   ('v2f/stream', list(chain(*self.bodyVerticies))),      # verticies
    #   ('c3f/static', self.colour * len(self.bodyVerticies)), # colour for each vertex (all the same)
    # )

    # self.vertexLists = [ self.bodyVertexList ]
    self.vertexLists = []

    # self.lineVertexList = game.engine.drawLayersBatch[self.drawLayer].add(
    #   2,
    #   gl.GL_LINES,
    #   None, # group
    #   ('v2f/stream', list(chain(*[self.pos, self.pos+Vec2d(30, 0).rotated(self.input.currentAim)]))),      # verticies
    #   ('c3f/static', self.lineColour * 2), # colour for each vertex (all the same)
    # )


  def draw(self):
    # self.bodyVertexList.vertices = list(chain(*[v*random.random()+self.body.position for v in self.bodyVerticies]))
    with shiftView(self.body.position):
      gl.glColor3f(*self.colour)
      gl.glBegin(gl.GL_TRIANGLE_FAN)
      # gl.glVertex2f(0, 0)
      # for i in xrange(0, 365, 5):
      #   gl.glVertex2f(*self.size.rotated_degrees(i))
      for point in self.bodyVerticies:
        gl.glVertex2f(*point)
      gl.glEnd()

  def __repr__(self):
    return 'Blob{0}'.format(self.id)
