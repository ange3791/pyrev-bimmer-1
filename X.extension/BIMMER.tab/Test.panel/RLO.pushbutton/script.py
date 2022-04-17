#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap
import revito as rvt
#from importlib import reload
#reload(rvt)

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
    pipe0 = DB.Electrical.Conduit.Create(doc, pipe1.GetTypeId(), cc0[0].Origin, cc0[1].Origin, pipe1.ReferenceLevel.Id)
    
    rvt.set_parameter_value_by_name(pipe0, "Diameter(Trade Size)", rvt.get_parameter_value(pipe1, "Diameter(Trade Size)"))

    cc1 = rvt.get_closest_connectors(pipe1, pipe0)
    doc.Create.NewElbowFitting(cc1[0], cc1[1])

    cc1 = rvt.get_closest_connectors(pipe2, pipe0)
    doc.Create.NewElbowFitting(cc1[0], cc1[1])

    t.Commit()
