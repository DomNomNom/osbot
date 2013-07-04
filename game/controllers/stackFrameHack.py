from pymunk import Vec2d

from base import Controller

import inspect

from game.utils import liveInspect


'''
A proof-of-concept Controller which shows
that it is really hard to secure against malicious code
that tries to modify the state directly.

We're all adults here, write proper code.
'''
class HAAAX(Controller):

  def actions(self, dt):
    try:
      frame = inspect.stack()[8][0]
      module = inspect.getmodule(frame)
      members = dict(inspect.getmembers(module))
      engine = members['engine']

      # now we could freely modify the engine
      for blob in engine.blobs.itervalues():
        blob.colour = (0,1,0)

    finally:
        del frame  # otherwise garbage collection gets slow

del HAAAX # remove the evil