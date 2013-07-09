import random

from pymunk import Vec2d, Space

import controllers

from Entities.Blob import Blob
from Entities.Wall import Wall
from Entities.Entity import PhysicsEntity

from math import sqrt, pi


# Initialize each class with a unique number and a bitmask for its collision layers
allPhysicsEntities = [Blob, Wall]

collisionLayers = [
  [Blob], # Blob with other Blobs
  [Blob, Wall] # bounce off walls
]

for i, physicsClass in enumerate(allPhysicsEntities):
  physicsClass.collisionType = i
  physicsClass.collisionBitmask = 0

# initialzie collisionBitmasks from the layers
for i, layerClasses in enumerate(collisionLayers):
  for physicsClass in layerClasses:
    physicsClass.collisionBitmask |= 2**i


engine = None
def createSpace(engine_):
  global engine
  engine = engine_

  space = Space()
  space.gravity = Vec2d(0.0, 0.0)
  PhysicsEntity.body = space.static_body

  # attach collision handlers (defined at the end of the file)
  space.add_collision_handler(
    Blob.collisionType,
    Blob.collisionType,
    # begin = handler_blob
    # separate = handler_blob
    pre_solve = handler_blob
  )
  # space.add_collision_handler(
  #   Blob.collisionType,
  #   Wall.collisionType,
  #   pre_solve = handler_wall,
  # )

  return space

massEjectProportion = 0.10  # 10% of the original mass gets ejected
def shoot(blob, ejectVel):
  if blob.radius < Blob.minRadius:
    return
  assert 0 < massEjectProportion < 1
  assert ejectVel
  mass_eject = blob.body.mass *      massEjectProportion
  mass_blob  = blob.body.mass * (1 - massEjectProportion)
  radius = sqrt(mass_eject / pi)
  offset = Vec2d(ejectVel)
  offset.length = blob.radius + radius + 0.0001

  originalVelocity = Vec2d(blob.body.velocity)
  blob.body.velocity = (mass_blob*blob.body.velocity - mass_eject*ejectVel) / (mass_blob)  # conservation of momentum
  blob.radius = sqrt(mass_blob / pi)

  return Blob(
    controllers.Controller,
    blob.body.position + offset,
    radius,
    ejectVel + originalVelocity
  )


def quadraticFormula(a, b, c):
  return (-b + sqrt(b**2 - 4*a*c)) / (2*a)

def handler_blob(space, arbiter, *args, **kwargs):

  blob_1 = engine.shapeToEntity[arbiter.shapes[0]]
  blob_2 = engine.shapeToEntity[arbiter.shapes[1]]
  # print 'omgwtf: ', repr(random.shuffle([blob_1, blob_2]))


  if    blob_1.radius > blob_2.radius:  big, sml = blob_1, blob_2
  elif  blob_1.radius < blob_2.radius:  big, sml = blob_2, blob_1
  else:
    blobs = [blob_1, blob_2]
    random.shuffle(blobs)
    big, sml = blobs
    print 'Collision with equal sizes between {0} and {1}'.format(blob_1.id, blob_2.id) # DEBUG

  big_mass = big.body.mass
  sml_mass = sml.body.mass
  P_big = big_mass * big.body.velocity
  P_sml = sml_mass * sml.body.velocity
  P = P_big + P_sml   # total momentum

  d = (big.body.position - sml.body.position).length # distance
  B = big.radius**2 + sml.radius**2 # == area / pi
  if d <= sqrt(B): # if we can't fit both, OMNOMNOM
    big.radius = sqrt(B)
    big.body.velocity = (P_big + P_sml) / (big_mass + sml_mass)  # conservation of momentum
    engine.removeEntity(sml) # DIE!
  else:
    newBigRadius = quadraticFormula(1, -d, -.5*(B-d**2)) # mathemagic to keep area consisteny and have the circles barely not touching
    if newBigRadius < big.radius: # we are clearly moving away from each other
      return False
    big.radius = newBigRadius
    sml.radius = d - newBigRadius

    transferred_mass = big.body.mass - big_mass
    big.body.velocity = (P_big + transferred_mass*sml.body.velocity) / (big_mass + transferred_mass)
    # conservation of momentum
    # big.body.velocity = Vec2d()

  return False
