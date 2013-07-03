from itertools import chain
from math import pi, sqrt

import pyglet.gl as gl
import pyglet

import pymunk
from pymunk import Vec2d

from Entity import PhysicsEntity
from game.Camera import shiftView


class Wall(PhysicsEntity):

  drawLayer = 'game'

  colour = (.3,) * 3

  circleStepsize = 10 # degrees for drawing

  minRadius = 1

  # pos is the center, size is the maximum distance from the center
  def __init__(self, pos, size):
    pos = Vec2d(pos)
    size = Vec2d(size)
    self.verticies = [ pos+offset for offset in [
      (-size.x, -size.y),
      (+size.x, -size.y),
      (+size.x, +size.y),
      (-size.x, +size.y),
    ]]
    self.hitbox = pymunk.Poly(self.body, self.verticies)
    self.hitbox.layers = Wall.collisionBitmask
    self.hitbox.collision_type = Wall.collisionType
    self.hitbox.elasticity = 0.9
    self.hitbox.friction   = 0.0
    self.shapes = [self.hitbox]



  def draw(self):
    gl.glColor3f(*self.colour)
    gl.glBegin(gl.GL_POLYGON)
    for point in self.verticies:
      gl.glVertex2f(*point)
    gl.glEnd()

  def __repr__(self):
    return 'Wall{0}'.format(self.id)
