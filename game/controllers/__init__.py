# this file exists so this folder is seen as a module to python
# we also define allControllers

import pkgutil
# from base import Controller
import inspect



allControllers = {} # from name to constructor
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    # add all Controllers in all submodules
    module = loader.find_module(module_name).load_module(module_name)
    allControllers.update(
        inspect.getmembers(module, lambda x: inspect.isclass(x) and hasattr(x, 'actions'))
    )

# initialize each class with a  colour
colours = [
    [ 0.40,  0.78,  0.16],
    [ 0.5,   0.5,   0.5 ],
    [ 0.78,  0.16,  0.70],
    [ 0.32,  0.16,  0.78],
    [ 0.42,  0.16,  0.78],
    [ 0.55,  0.78,  0.16],
    [ 0.48,  0.16,  0.78],
    [ 0.50,  0.78,  0.16],
    [ 0.64,  0.16,  0.78],
    [ 0.36,  0.16,  0.78],
    [ 0.16,  0.78,  0.20],
    [ 0.74,  0.16,  0.78],
    [ 0.78,  0.16,  0.33],
    [ 0.78,  0.16,  0.46],
    [ 0.16,  0.78,  0.16],
    [ 0.16,  0.78,  0.32],
    [ 0.16,  0.70,  0.78],
    [ 0.54,  0.78,  0.16],
    [ 0.78,  0.68,  0.16],
    [ 0.78,  0.43,  0.16],
    [ 0.16,  0.78,  0.28],
    [ 0.78,  0.16,  0.51],
    [ 0.16,  0.78,  0.58],
    [ 0.78,  0.16,  0.64],
    [ 0.78,  0.16,  0.34],
    [ 0.29,  0.16,  0.78],
    [ 0.78,  0.16,  0.42],
    [ 0.16,  0.31,  0.78],
    [ 0.78,  0.23,  0.16],
    [ 0.29,  0.78,  0.16],
]
for colour, controller in zip(colours, allControllers.itervalues()):
    controller.colour = colour

Controller = allControllers['Controller']