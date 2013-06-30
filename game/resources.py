# for saving and loading
from ast import literal_eval
from pyglet import resource
from pyglet.resource import file as resourceOpen
from pymunk import Vec2d, Space




basePath = 'game/resources/'
resource.path = [basePath]
resource.reindex()

# a flag to chrash when anything goes wrong when the level isn't valid
chrashOnFail = True # TODO: move this to a config


# Entities
from Entities.Blob import Blob
constructors = { # To construct the entities when we load a level from a file
  'Blob' : Blob,
}




def loadEntities(levelName):
  lineCount = 0
  entities = []
  with resourceOpen('levels/'+levelName+'.txt') as levelFile:
    for line in levelFile:
      lineCount += 1
      lineErr = "(line " + str(lineCount) + ")"
      if len(line.strip()) == 0:       continue # skip blank lines
      if line.strip().startswith('#'): continue # skip comment lines

      try:
        data = literal_eval(line)
      except:
        print lineErr, "This line could not be parsed:", line
        continue

      entityType, args = data[0], data[1:]
      if entityType not in Level.constructors:
        print lineErr, "This is not a valid entity type:", entityType
        print lineErr, "Possible types:", Level.constructors.keys()
        continue
      constructor = self.constructors[entityType]

      try:
        newEntity = constructor(self, *args)
      except:
        print lineErr, "Constructing", entityType, "failed. probably weird arguments:", args
        if self.chrashOnFail: raise  # TODO: test me!
        continue

      entities.append(newEntity)

  return entities


# def save(self):
#   assert self.levelName
#   # TODO: test whether this will create folders
#   with resourceOpen('Levels/uncompressed/'+self.levelName+'/level.txt', 'w') as f:
#     f.write('{0}\n'.format(repr(entity)))
