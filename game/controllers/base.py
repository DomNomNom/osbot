
from pymunk import Vec2d

'''
Rules of a Controller:
- may not change the state of the program directly
- may not chrash or cause errors
- if it shoots too often, causing the Blob to become too small (<Blob.minRadius), it will no longer be run
- eject velocities will be externally clamped to have a magnitude <= physics.maxEjectVel
'''


class Controller(object):

  # colour = (1., 0., 1.) # will automatically be set for each class by __init__.py

  def __init__(self, blob, blobs, spaceView):
    self.blob  = blob
    self.blobs = blobs
    self.spaceView = spaceView
    self.start()

  def start(self):
    pass  # To override at your leasure (so you don't have to worry about the constructor)

  def actions(self, dt):
    return { 'shots': [] }
