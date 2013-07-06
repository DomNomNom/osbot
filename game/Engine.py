import time
import math


import pyglet.gl as gl
from pyglet.graphics import Batch
from pyglet.window import Window, key
from pyglet import clock
from pymunk import Vec2d

from Camera import Camera

import physics
import resources
import Entities
import levelCreator
from Entities.Blob import Blob
from utils import liveInspect


# a function to test whether physics values are in acceptable bounds
def assertClose(a, b):
  errorMargin = (abs(a)+abs(b))*0.0001 + 0.0001
  assert abs(a-b) <= errorMargin, "physics error. should be {0} but is {1}".format(a,b)


class Engine:

  def __init__(self):
    self.updateRate = 1/60. # how often our physics will kick in (in seconds)

    # groups of entities
    self.groups = {
      'all'       : set(),
      'updating'  : set(), # all that have a update function
    }

    self.entityAddQueue = []
    self.entityDelQueue = []

    # layers specify the order in which they are drawn. (ordered back to front)
    self.drawLayerNames = [
      'background',
      'game',
      'foreground',
      # UI ones from here on
      # UI Entities will be drawn in camera space
      'UI_pauseMenu',
      'UI_debug',
    ]

    # A dict from drawLayerNames to a Batch of entities. they are mutually exclusive
    self.drawLayers = { name : Batch()  for name in self.drawLayerNames }
    self.drawCalls =  { name : []       for name in self.drawLayerNames }

    self.levelStartTime = time.time()
    self.levelTime = 0. # TODO proper pausing (maybe move to gameState or some level class)

    self.accumulatedFrameTime = 0.

    self.shapeToEntity = {} # a dict that gives the entity that contains the keyed shape
    self.blobs = {}         # a dict from blob.id to blob
    self.highestBlobId = 0

    # Window
    config = gl.Config(
      sample_buffers=1, samples=4   # antialiasing
    )
    self.window = Window(
      config = config,
      #fullscreen = True,
      vsync = False,
      style = Window.WINDOW_STYLE_BORDERLESS,
    )

    # opengl flags
    gl.glEnable(gl.GL_BLEND) #enables transparency

    # mouse position
    self.windowCenter = Vec2d(self.window.get_size()) / 2
    self.mousePos = Vec2d(self.windowCenter)
    @self.window.event
    def on_mouse_motion(x, y, dx, dy):
      self.mousePos.x = x
      self.mousePos.y = y
    @self.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
      self.mousePos.x = x
      self.mousePos.y = y

    # DEBUG: drop us into a debug shell when
    @self.window.event
    def on_key_press(symbol, modifiers):
      if symbol==key.QUOTELEFT and modifiers & key.MOD_CTRL:
        liveInspect(self)

    self.fps_display = clock.ClockDisplay()

    # camera
    self.camera = Camera()


    # shedule our main loop so we don't need to manually deal with time
    clock.schedule(self.run)


  # our main game loop
  def run(self, dt):
    ## UPDATE ##
    # timestep ala http://gafferongames.com/game-physics/fix-your-timestep/
    if dt > .25: # avoid spiral of death (updating taking longer than framerate)
      dt = .25
    self.accumulatedFrameTime += dt
    while self.accumulatedFrameTime >= self.updateRate:
      self.accumulatedFrameTime -= self.updateRate
      self.levelTime = time.time() - self.levelStartTime
      for entity in self.groups['updating']:
        # update all entities, this should not change the state
        response = entity.update(self.updateRate)
        if response:
          self.entityAddQueue += response.get("add Entities", [])
          self.entityDelQueue += response.get("del Entities", [])
      self._processRemoving()
      self._processAdding()

      self.space.step(self.updateRate) # this will do the physics and apply all actions
      self._processRemoving()
      self._processAdding()

      # DEBUG: test for physics consistency. Disabled as bouncing off Walls changes momentum
      # momentum =                        sum([ e.body.mass * e.body.velocity for e in self.blobs.itervalues() ])
      assertClose(self.physCheck_mass,  sum([ e.body.mass                   for e in self.blobs.itervalues() ]))
      assertClose(self.physCheck_area,  sum([ math.pi * e.radius**2         for e in self.blobs.itervalues() ]))
      # assertClose(self.physCheck_mometum.x, momentum.x)
      # assertClose(self.physCheck_mometum.y, momentum.y)


    ## DRAW ##
    gl.glClearColor(0,0,0, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()

    self.camera.track() # does camera work (such as what it focuses on)
    for name in self.drawLayerNames:
      for func in self.drawCalls[name]:
        func()
      # shift = Vec2d() if name.startswith('UI') else None
      # with self.camera.shiftView(shift):
      #   self.drawLayers[name].draw()


    self.fps_display.draw()
    #self.window.flip()

  def loadLevel(self, levelName):
    # Initialize physics
    self.space = physics.createSpace(self)

    # self.levelCreator = resources.loadEntities
    self.levelCreator = levelCreator.createLevel

    # load the entities
    for e in self.levelCreator(levelName):
      self.addEntity(e)

    self._processAdding()
    self._processRemoving()

    self.physCheck_mass     = sum([ e.body.mass                   for e in self.blobs.itervalues() ])
    self.physCheck_area     = sum([ math.pi * e.radius**2         for e in self.blobs.itervalues() ])
    self.physCheck_mometum  = sum([ e.body.mass * e.body.velocity for e in self.blobs.itervalues() ])

  def addEntity(   self, e):  self.entityAddQueue.append(e)
  def removeEntity(self, e):  self.entityDelQueue.append(e)


  def _processAdding(self):
    while len(self.entityAddQueue):
      e = self.entityAddQueue.pop(0)
      self.groups["all"].add(e)
      if Entities.isEntityKind_updating(e):   self.groups['updating'].add(e)
      if Entities.isEntityKind_physics(e):
        self.space.add(e.shapes)
        for shape in e.shapes:
          self.shapeToEntity[shape] = e
        if e.body is not self.space.static_body:
          self.space.add(e.body)
      if Entities.isEntityKind_visible(e):
        # e.setupVertexLists(self.drawLayers[e.drawLayer])
        # assert hasattr(e, 'vertexLists')
        if hasattr(e, 'draw'):
          self.drawCalls[e.drawLayer].append(e.draw)
      if isinstance(e, Blob):
        self.highestBlobId += 1
        e.controller = e.controller(e, self.blobs)  # initialize the controller
        e.id = self.highestBlobId
        self.blobs[e.id] = e

  def _processRemoving(self):
    while len(self.entityDelQueue):
      e = self.entityDelQueue.pop(0)
      if e in self.groups['all']:
        self.groups['all'].remove(e)
      else:
        print "was told to delete entity but it was not in the 'all' group: " + repr(e) # DEBUG
        continue
      if Entities.isEntityKind_updating(e):   self.groups['updating'].remove(e)
      if Entities.isEntityKind_physics(e):
        self.space.remove(e.shapes)
        for shape in e.shapes:
          del self.shapeToEntity[shape]
        if e.body is not self.space.static_body:
          self.space.remove(e.body)
      if Entities.isEntityKind_visible(e):
        # self.drawLayers[e.drawLayer].remove(e)
        if hasattr(e, 'draw'):
          self.drawCalls[e.drawLayer].remove(e.draw)
        # for vertexList in e.vertexLists:
        #   vertexList.delete()
      if isinstance(e, Blob):
        del self.blobs[e.id]
