
from pymunk import Vec2d, Space


from Entities.Blob import Blob
from Entities.Entity import PhysicsEntity



# Initialize each class with a unique number and a bitmask for its collision layers
allPhysicsEntities = [Blob]

collisionLayers = [
  [Blob], # Blob with other Blobs
]

for i, physicsClass in enumerate(allPhysicsEntities):
  physicsClass.collisionType = i
  physicsClass.collisionBitmask = 0

for i, layerClasses in enumerate(collisionLayers):
  for cls in layerClasses:
    physicsClass.collisionBitmask += 2**i


shapeToEntity = {}
def createSpace(shapeToEntityMap):
  global shapeToEntity
  shapeToEntity = shapeToEntityMap
  space = Space()
  space.gravity = Vec2d(0.0, 0.0)
  PhysicsEntity.body = space.static_body


  # attach collision handlers (defined at the end of the file)
  # space.add_collision_handler(
  #   Rocket.collisionType,
  #   Platform.collisionType,
  #   begin = rocketHandler
  # )

  return space

def handler_blob(space, arbiter, *args, **kwargs):
  blob_1 = game.engine.shapeToEntity[arbiter.shapes[0]]
  rocket.explode()
  game.engine.removeEntity(rocket)
  return False
