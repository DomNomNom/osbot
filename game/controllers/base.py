
from pymunk import Vec2d

'''
Rules of a Controller:
- may not change the state of the program directly
- may not chrash cause errors
- if it shoots to often, causing the Blob to become too small ( < Blob.minRadius), it will no longer be run
'''


class Controller(object):

  def __init__(self, blob, blobs):
    self.blob  = blob
    self.blobs = blobs
    self.start()

  def start(self):
    pass  # To override at your leasure (so you don't have to worry about the constructor)

  def actions(self, dt):
    return { 'shots': [] }



class ShootPeriodically(Controller):
  def start(self):
    self.time = 0
    self.shoot_interval = 0.2
    self.shoot_next = self.shoot_interval

  def actions(self, dt):
    self.time += dt
    if self.time >= self.shoot_next:
      self.shoot_next += self.shoot_interval
      return { 'shots' : [Vec2d(100,0)] }
    return {}

