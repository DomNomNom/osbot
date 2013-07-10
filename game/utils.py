from code import InteractiveConsole


def liveInspect(locals):
    if not isinstance(locals, dict):
        locals = {"t": locals}
    ic = InteractiveConsole(locals)
    try:
      ic.interact("Welcome to the live inspect console! press ctrl+D to resume the game\n your locals are {0}".format(locals))
    except SystemExit, e:
      return #exit()