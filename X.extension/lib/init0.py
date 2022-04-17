import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

uiapp = __revit__
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument
doc = uidoc.Document

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
#from Autodesk.Revit.UI import UIDocument, Selection

'''
from math import sin, cos, floor, modf
from toolz.curried import pipe, map, filter, reduce
from operator import itemgetter
import pandas as pd
from timeit import default_timer as timer
from pyrevit import output
'''

#from math import modf
#from toolz.curried import pipe, map, filter, reduce
#import Autodesk.Revit.DB as DB



categories = ("OST_CableTray", "OST_CableTrayFitting", "OST_Conduit", "OST_ConduitFitting", "OST_DuctCurves", "OST_DuctFitting", "OST_DuctTerminal", "OST_ElectricalEquipment", "OST_ElectricalFixtures", "OST_LightingDevices", "OST_LightingFixtures", "OST_MechanicalEquipment", "OST_PipeCurves", "OST_PipeFitting", "OST_PlumbingFixtures", "OST_SpecialtyEquipment", "OST_Sprinklers", "OST_Wire")
classes = ("CableTray", "Conduit", "Duct", "Pipe")
attribs = ("Floor", "FootPrintRoof")
