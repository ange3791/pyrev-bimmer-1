#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap

from general_funcs import iff

import revito as rvt
#from importlib import reload
#reload(rvt)


#DB.BuiltInCategory
#   OST_PipeCurvesCenterLine
#   OST_PipeFittingCenterLine
#   OST_ConduitCenterLine
#   OST_ConduitFittingCenterLine

#Drops
#   OST_ConduitDrop
#   OST_ConduitRiseDrop



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

