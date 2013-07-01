# this file exists so this folder is seen as a module to python

# return whether e has conditionAttr
# if it does, check that e also has the sideAttrs
def hasAttrs(e, conditionAttr, *sideAttrs):
  if hasattr(e, conditionAttr):
    for attr in sideAttrs:
      assert hasattr(e, attr)
    return True
  return False

# ducktype tests
def isEntityKind_physics(e):  return hasAttrs(e, 'body', 'shapes')
def isEntityKind_visible(e):  return hasAttrs(e, 'drawLayer', 'vertexLists')
def isEntityKind_updating(e): return hasAttrs(e, 'updating')
