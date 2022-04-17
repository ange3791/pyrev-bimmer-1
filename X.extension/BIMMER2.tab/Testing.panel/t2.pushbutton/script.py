#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap

from general_funcs import iff

import revito as rvt
from importlib import reload
reload(rvt)
#from pyrevit import output

try:
    sel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

#param_values = pipe(    params,
#                        filter(lambda x: rvt.get_parameter_value(sel, x) is not None),
#                        map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)

except:
    sel = None



#s1 = {"a", "b", ("5", 6), 3}
#print(len(s1))
#pipes = rvt.connected(sel, set())

#for pipe in pipes:
#    print(pipe)


pipes1 = rvt.connected_x(sel, set(), set())

for p in pipes1:
    print(p)
#print(len(pipes1))
