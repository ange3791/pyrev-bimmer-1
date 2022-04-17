#! python3

from init0 import *
import revito as rvt
#from importlib import reload
#import general_funcs
#reload(general_funcs)
from general_funcs import conc, list_count, left
from toolz.curried import pipe, map, filter
from os import path
from collections import Counter
#import pandas as pd


'''
project_name = doc.ProjectInformation.Name
ConduitUse = "FDR"
fname = conc(path.expanduser("~"), "\\Desktop\\", project_name, "-ConduitRunSchedule-", ConduitUse, ".csv")

print(f'Path name: {fname}')
#print(f'X: {DB.ProjectInfo.Name}')
'''
print(f'Blue Bangers in this View')

print("------------------------")
print(f'By Family Name and Type')

BBs = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
                    map(lambda x: x.Name),
                    tuple)

for i in sorted(list_count(BBs)):
    print(f'{i[0]}: {i[1]}')

print("------------------------")
print(f'By Type Mark')
BBs_by_typemark = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: left(rvt.get_parameter_value(x.Symbol, "Type Mark"), 2) == "BB"),
                    map(lambda x: rvt.get_parameter_value(x.Symbol, "Type Mark")),
                    tuple)

for i in sorted(list_count(BBs_by_typemark)):
    print(f'  {i[0]}: {i[1]}')



#BB1s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
#                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
#                    #filter(lambda x: rvt.get_parameter_value(x, "Comments") == "Conduit Support"),
#                    tuple)
#print(f'BB1s: {len(BB1s)}')

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

BB2s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Rod - Point Assembly_bluebanger"),
                    tuple)
print(f'BB2s: {len(BB2s)}')


BB3s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Junction Boxes - Load"),
                    tuple)
#BB3s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements(),
#                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Junction Boxes - Load"),
#                    tuple)
print(f'BB3s: {len(BB3s)}')


BB4s = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    #filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
                    filter(lambda x: x.Name == "BLUE BANGER - TEMP"),
                    tuple)
print(f'BB4s: {len(BB4s)}')
'''

#for x in BB3s:
#    print(x.

#BB1 = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements(),
#                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
#                    map(lambda x: x.Name),
#                    #filter(lambda x: x.Name == "Lighting Support"),
#                    tuple)


'''
#x = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(),
#BBs = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc, view.Id), DB.BuiltInCategory.OST_ElectricalFixtures, "ElementIsNotType"),
#X = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
trapezes = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "MCE HANGER"),
                    tuple)
print(f'Trapeze hanger: {len(trapezes)}')

X = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_LightingFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Pendant Light - Disk"),
                    tuple)
print(f'Pendant Light - Disk: {len(X)}')


X = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_LightingFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Pendant"),
                    tuple)
print(f'Pendant: {len(X)}')


X = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_LightingFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "Pendant Lighting Fixture1"),
                    tuple)
print(f'Pendant Lighting Fixture1: {len(X)}')



trapeze_bangers = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
                    filter(lambda x: x.Name == "Trapeze"),
                    tuple)
print(f'Trapeze bangers: {len(trapeze_bangers)}')


bangers = pipe(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements(),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "BLUE BANGER"),
                    map(lambda x: x.Name),
                    #filter(lambda x: x.Name == "Lighting Support"),
                    tuple)

def countme(list_in):
    list_out = list()
    for i in set(list_in):
        list_out.append([i, list_in.count(i)])

    return list_out

for i in countme(bangers):
    print(f'{i[0]}: {i[1]}')


'''
