import random

from pymunk import Vec2d

from base import Controller


# class ShootPeriodically(Controller):
#   def start(self):
#     self.time = 0
#     self.shoot_interval = 0.2
#     self.shoot_next = self.shoot_interval

#   def actions(self, dt):
#     self.time += dt
#     while self.time >= self.shoot_next:
#       self.shoot_next += self.shoot_interval
#       return { 'shots' : [Vec2d(100,0)] }
#     return {}

class ShootRandomly(Controller):
  def start(self):
    self.time = 0
    self.shoot_interval = 0.2
    self.shoot_next = self.shoot_interval

  def actions(self, dt):
    self.time += dt
    while self.time >= self.shoot_next:
      self.shoot_next += self.shoot_interval
      return { 'shots' : [Vec2d(100,0).rotated(random.random()*360)] }
    return {}