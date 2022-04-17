#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap

from general_funcs import iff

import revito as rvt
#from importlib import reload
#reload(rvt)

'''
try:
    pipe1 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))
    pipe2 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

except:
    pipe1 = None
    pipe2 = None


if pipe1 is not None and pipe2 is not None:
    t = DB.Transaction(doc, 'Connect to')
    t.Start()
    #pipe3 = DB.Plumbing.Pipe.Create(doc, get_pipe_PipingSystemTypeId(pipe1), get_pipe_PipeType(pipe1).Id, get_pipe_Level(pipe1).Id, p1, p2)
    cc0 = rvt.get_closest_connectors(pipe1, pipe2)
    cc0[0].ConnectTo(cc0[1])
    #pipe0 = DB.Plumbing.Pipe.Create(doc, rvt.get_pipe_PipeType(pipe1).Id, rvt.get_pipe_Level(pipe1).Id, cc0[0], cc0[1])
    #cc1 = rvt.get_closest_connectors(pipe1, pipe0)
    #doc.Create.NewElbowFitting(cc1[0], cc1[1])
    #cc1 = rvt.get_closest_connectors(pipe2, pipe0)
    #doc.Create.NewElbowFitting(cc1[0], cc1[1])

    t.Commit()
'''


view = uidoc.ActiveView
fitting_cl_id = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_PipeFittingCenterLine).Id
pipe_cl_id = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_PipeCurvesCenterLine).Id

fitting_cl_id_visible = view.GetCategoryHidden(fitting_cl_id)
pipe_cl_id_visible = view.GetCategoryHidden(pipe_cl_id)



t = DB.Transaction(doc, 'Change centerline visibility')
t.Start()

if view.IsCategoryOverridable(pipe_cl_id):
    v = view

else:
    v = doc.GetElement(view.ViewTemplateId)

v.SetCategoryHidden(pipe_cl_id, not pipe_cl_id_visible)
v.SetCategoryHidden(fitting_cl_id, not fitting_cl_id_visible)

t.Commit()

