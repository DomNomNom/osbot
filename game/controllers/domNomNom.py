import pymunk
from pymunk import Vec2d

from base import Controller


def dangerous(blob, other):
  from game.Entities.Blob import Blob
  if (
    not issubclass(type(other), Blob) or
    other.radius < blob.radius
  ):
    return False

  # look at the other from our blobs perspective, and see whether he will touch us
  # we assume linear motion for both of us
  # http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Vector_formulation
  relVel = other.body.velocity - blob.body.velocity
  n = relVel.normalized()
  a = other.body.position
  p = blob.body.position

  dot = n.dot(a-p)
  if dot > 0: # the collision is in the past
    return False

  projection = dot * n
  minDistOffset = (a-p) - projection

  if minDistOffset.length > other.radius + blob.radius:
    return False

  return True


class DomNomNom(Controller):
  def start(self):
    self.hitTest = pymunk.Circle(self.spaceView.body, self.blob.radius)
    self.detectionRadius = 100


  def actions(self, dt):
    # self.time += dt
    # while self.time >= self.shoot_next:
    #   self.shoot_next += self.shoot_interval
    #
    self.hitTest.unsafe_set_offset(self.blob.body.position)
    self.hitTest.unsafe_set_radius(self.blob.radius + self.detectionRadius)
    others = self.spaceView.shape_query(self.hitTest)
    happy = True
    if len(others) > 1:
      others.remove(self.blob.hitbox)
      dangerousBlobs = [ other for other in others if dangerous(self.blob, self.spaceView.shapeToEntity[other]) ]
      if dangerousBlobs:
        # print 'omg about to be eaten:', dangerousBlobs
        happy = False
        self.colour = (1,0,0)
        return { 'shots' : [ 100 * (danger.body.position-self.blob.body.position) for danger in dangerousBlobs ] }

    self.colour = (0,1,0)
    return {}