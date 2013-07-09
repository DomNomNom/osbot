from itertools import chain
from math import pi, sqrt

import pyglet.gl as gl
import pyglet

import pymunk
from pymunk import Vec2d

from Entity import PhysicsEntity
from game.Camera import shiftView
import game.controllers as controllers


class Blob(PhysicsEntity):

  drawLayer = 'game'

  softBorderRadius = 5 # how many pixels on the sides are just for a soft border?

  # if smaller than this,
  # the AI will not be run and no further propulsion is allowed
  minRadius = 10

  texture = pyglet.resource.image('blob.png')

  # radius. (getter/setter)
  def radius_get(self):  return self._radius
  def radius_set(self, radius):
    assert radius > 0
    self._radius = radius
    self.hitbox.unsafe_set_radius(radius)
    self.body.mass = pi * radius**2
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
          'shots' : actions['shots']
        }

    return {}


  def initGraphics(self, batch):
    # TODO: use the controllers texture
    self.sprite = pyglet.sprite.Sprite(Blob.texture, batch=batch)
    self.sprite.color = self.controller.colour


  def draw(self):
    self.sprite.color = [ x*255 for x in self.controller.colour ]
    self.sprite.scale = self.radius*2 / (Blob.texture.width - 2*self.softBorderRadius)
    self.sprite.set_position(
      self.body.position.x - self.radius - self.softBorderRadius*self.sprite.scale + 1,
      self.body.position.y - self.radius - self.softBorderRadius*self.sprite.scale + 1,
    ) # note: the +1 at the end seems to make it more accurate to the old-style

    # with shiftView(self.body.position):
    #   self.label.font_size = self.radius * .5
    #   self.label.text = str(self.id)
    #   self.label.draw()

  def __repr__(self):
    return 'Blob{0}'.format(self.id)
