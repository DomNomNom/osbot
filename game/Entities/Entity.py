
class PhysicsEntity(object):
  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)

  body = None # This default class variable will be set by the Engine to space.static_body