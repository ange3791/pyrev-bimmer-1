#! python3

from init0 import *


#import init0
#reload(init0)

#import general_funcs as gf
#reload(gf)

#from general_funcs import iff

import revito as rvt
#from importlib import reload


#from toolz.curried import pipe, map, filter
#from general_funcs import conc, list_count

#import init0

#import general_funcs

#from general_funcs import iff
sel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

print(rvt.get_parameter_value(sel, "TO"))


#import pandas as pd

'''
x1 = pipe(DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Conduits).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x, "PANEL NAME") == "RP2-2"),
                    map(lambda x: tuple([   rvt.get_parameter_value(x, "PANEL NAME"),
                                            rvt.get_parameter_value(x, "FR"),
                                            rvt.get_parameter_value(x, "TO"),
                                            ])),
                    #filter(lambda x: rvt.get_parameter_value(x, "Comments") == "Conduit Support"),
                    tuple)
'''


'''
BB1s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER" and x.Name == "BLUE BANGER - Hangers"),
                    #filter(lambda x: rvt.get_parameter_value(x, "Comments") == "Conduit Support"),
                    tuple)
print(f'BB1s: {len(BB1s)}')


#B2s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements(),
#                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER" and x.Name == "BLUE BANGER_lighting support"),
#                    filter(lambda x: rvt.get_parameter_value(x, "Comments") == "Lighting Support"),
#                    tuple)
#print(f'BB2s: {len(BB2s)}')


def countme(list_in):
    list_out = list()
    for i in set(list_in):
        list_out.append([i, list_in.count(i)])

    return list_out

for i in countme(bangers):
    print(f'{i[0]}: {i[1]}')


'''
