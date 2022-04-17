#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap
import revito as rvt
from importlib import reload
reload(rvt)

from general_funcs import iff



#from pyrevit import output
try:
    pipe1 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))
    pipe2 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

except:
    pipe1 = None
    pipe2 = None


if pipe1 is not None and pipe2 is not None:
    t = DB.Transaction(doc, 'Create rolling offset')
    t.Start()
    #pipe3 = DB.Plumbing.Pipe.Create(doc, get_pipe_PipingSystemTypeId(pipe1), get_pipe_PipeType(pipe1).Id, get_pipe_Level(pipe1).Id, p1, p2)
    cc0 = rvt.get_closest_connectors(pipe1, pipe2)
    pipe0 = DB.Plumbing.Pipe.Create(doc, rvt.get_pipe_PipeType(pipe1).Id, rvt.get_pipe_Level(pipe1).Id, cc0[0], cc0[1])


    cc1 = rvt.get_closest_connectors(pipe1, pipe0)
    doc.Create.NewElbowFitting(cc1[0], cc1[1])

    cc1 = rvt.get_closest_connectors(pipe2, pipe0)
    doc.Create.NewElbowFitting(cc1[0], cc1[1])

    t.Commit()
