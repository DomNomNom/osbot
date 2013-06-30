from Entity import PhysicsEntity


class Blob(PhysicsEntity):


  def __init__(self, pos, radius):
    self.pos = pos
    self.radius = radius

    self.hitbox = pymunk.Circle(self.body, self.size.x)
    # note: collisionLayers and collisionType get created by physics.py
    self.hitbox.friction = 1
    self.hitbox.layers = Blob.collisionLayers
    self.hitbox.collision_type = Blob.collisionType
    self.shapes = [self.hitbox]

    # vertex lists
    self.bodyVerticies = [Vec2d()]
    for i in xrange(0, 365, 5):
      self.bodyVerticies.append(self.size.rotated_degrees(i))
    self.bodyVertexList = game.engine.drawLayersBatch[self.drawLayer].add(
      len(self.bodyVerticies),
      gl.GL_TRIANGLE_FAN,
      None, # group
      ('v2f/stream', list(chain(*self.bodyVerticies))),      # verticies
      ('c3f/static', self.colour * len(self.bodyVerticies)), # colour for each vertex (all the same)
    )

    # self.lineVertexList = game.engine.drawLayersBatch[self.drawLayer].add(
    #   2,
    #   gl.GL_LINES,
    #   None, # group
    #   ('v2f/stream', list(chain(*[self.pos, self.pos+Vec2d(30, 0).rotated(self.input.currentAim)]))),      # verticies
    #   ('c3f/static', self.lineColour * 2), # colour for each vertex (all the same)
    # )

    self.vertexLists = [self.bodyVertexList, self.lineVertexList]
