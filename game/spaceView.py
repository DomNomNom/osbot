

# Should be treated as an immutuable view a space.
# It has some nice functions that would be conventient for controllers
class SpaceView(object):
    def __init__(self, space):
        self.shape_query = space.shape_query
        self.body = space.static_body # for hit-test shapes
        self.shapeToEntity = {} # a dict that gives the entity that contains the keyed shape