# this file exists so this folder is seen as a module to python
# we also define allControllers

import pkgutil
from base import Controller
import inspect

allControllers = {} # from name to constructor
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    # add all Controllers in all submodules
    module = loader.find_module(module_name).load_module(module_name)
    allControllers.update(
        inspect.getmembers(module, lambda x: inspect.isclass(x) and hasattr(x, 'actions'))
    )
