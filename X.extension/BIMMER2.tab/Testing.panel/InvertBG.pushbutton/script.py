#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap
from revito import *
from general_funcs import iff

#from pyrevit import output

#get fixtures and specialty equipment
#try:
    #all_picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")
    #picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")

#except:
#    pass

#import Autodesk.Revit as AR
#print(AR.ApplicationServices.Application.BackgroundColor)
print(DB.ColorOptions.BackgroundColor.GetValue)
#print("sdfsdf")
