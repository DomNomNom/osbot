from itertools import chain
from math import pi, sqrt

import pyglet.gl as gl
import pyglet

import pymunk
from pymunk import Vec2d

from Entity import PhysicsEntity
from game.Camera import shiftView
from game.controllers.base import Controller


class Blob(PhysicsEntity):

  drawLayer = 'game'

  colour = (1, 0, 0)

  circleStepsize = 10 # degrees for drawing

  minRadius = 5

  def radius_get(self):  return self._radius
  def radius_set(self, radius):
    assert radius > 0
    self._radius = radius
    self.hitbox.unsafe_set_radius(radius)
    self.body.mass = pi * radius**2
    self.radiusVector = Vec2d(radius, 0)
    self.circleStepsize = int(0.9*360/radius)
    self.bodyVerticies = [Vec2d()] # recalculate verticies (this could be done with a matrix transform)
    for i in xrange(0, 360+self.circleStepsize, self.circleStepsize):
      self.bodyVerticies.append(self.radiusVector.rotated_degrees(i))
  radius = property(radius_get, radius_set)



  def __init__(self, controller, pos, radius, vel=None):
    self.controller = controller
    self.body = pymunk.Body(mass=pi*radius**2, moment=float('inf'))
    self.body.position = Vec2d(pos)
    self.body.velocity = Vec2d(vel)
    self.hitbox = pymunk.Circle(self.body, radius)
    self.hitbox.layers = Blob.collisionBitmask
    self.hitbox.collision_type = Blob.collisionType
    self.hitbox.elasticity = 0.9
    self.shapes = [self.hitbox]

    self.radius = radius # note: calls setter
    #self.id = id(self) # set by Engine

    self.label = pyglet.text.Label(
      'OMG',
      font_name='Times New Roman',
      font_size=12,
      x=0, y=2,
      anchor_x='center', anchor_y='center'
    )

    self.firstTimeRender = True


  def update(self, dt):
    if self.radius >= self.minRadius:
      actions = self.controller.actions(dt)

      if actions and 'shots' in actions:
        return {
          'add Entities' : [ self.shoot(ejectVel) for ejectVel in actions['shots'] ]
        }
    # else:
    #   print 'too small'

    return {}

  def shoot(self, ejectVel):
    massEjectProportion = 0.10  # 10%
    assert 0 < massEjectProportion < 1
    assert ejectVel
    mass_eject = self.body.mass *      massEjectProportion
    mass_self  = self.body.mass * (1 - massEjectProportion)
    radius = sqrt(mass_eject / pi)
    offset = Vec2d(ejectVel)
    offset.length = self.radius + radius + 0.0001


    originalVelocity = Vec2d(self.body.velocity)
    self.body.velocity = (mass_self*self.body.velocity - mass_eject*ejectVel) / (mass_self)  # conservation of momentum
    self.radius = sqrt(mass_self / pi)


    return Blob(
      Controller,
      self.body.position + offset,
      radius,
      ejectVel + originalVelocity
    )

  def draw(self):
    with shiftView(self.body.position):
      gl.glColor3f(*self.colour)
      gl.glBegin(gl.GL_TRIANGLE_FAN)
      for point in self.bodyVerticies:
        gl.glVertex2f(*point)
      gl.glEnd()

      # self.label.font_size = self.radius * .5
      self.label.text = str(self.id)
      self.label.draw()

  def __repr__(self):
    return 'Blob{0}'.format(self.id)
