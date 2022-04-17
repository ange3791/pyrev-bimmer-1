#! python3

from init0 import *
import revito as rvt
from general_funcs import conc, type_of
from toolz.curried import pipe, map, filter
from os import path
from collections import Counter
#import pandas as pd


project_name = doc.ProjectInformation.Name
ConduitUse = "FDR"
fname = conc(path.expanduser("~"), "\\Desktop\\", project_name, "-ConduitRunSchedule-", ConduitUse, ".csv")

print(f'Path name: {fname}')
#print(f'X: {DB.ProjectInfo.Name}')



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



    return list_out

for i in countme(bangers):
    print(f'{i[0]}: {i[1]}')
'''

#print(f'{i}: {bangers.count(i)}')


#print(f'All BBs: {len(bangers)}')
#x1 = Counter(bangers)
#print(x1)

#x1 = pd.Series(bangers).value_counts
#print(x1)
#for i in x1:
#    print(i)


        #params = floor.Parameters
        #for p in params:
        #    print(f'_______{p.Definition.Name}={parameter_value(p)}')


#conduit_runs = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ConduitRun).WhereElementIsNotElementType().ToElements()
#conduit_runs = DB.FilteredElementCollector(doc).OfClass(DB.Electrical.CableTrayConduitRunBase).WhereElementIsNotElementType().ToElements()

#print(conduit_runs[111].GetDependentElements(None))

#for conduit_run in conduit_runs:
#    print(f'{conduit_run.Id}')

#conduits = pipe(all_elements_of_category(DB.FilteredElementCollector(doc), DB.BuiltInCategory.OST_ConduitFitting, "ElementIsNotType"),
#conduits = pipe(all_elements_of_category(DB.FilteredElementCollector(doc), DB.BuiltInCategory.OST_Conduit, "ElementIsNotType"), tuple)

#Temp fix: Set Fecheckbox
#conduit_pipes = pipe(DB.FilteredElementCollector(doc,uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(), tuple)

'''
conduit_pipes = pipe(DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(), tuple)
conduit_fittings = pipe(DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ConduitFitting).WhereElementIsNotElementType().ToElements(), tuple)
conduits = conduit_pipes + conduit_fittings

print(len(conduit_pipes))
print(len(conduit_fittings))
print(len(conduits))

#t = DB.Transaction(doc, 'fix')
#t.Start()

changed = 0
for p in conduits:
    #get_parameter_value(p, "F")

    if left(get_parameter_value(p, "Comments"), 3) == "FDR":
        val = "FDR"
    elif left(get_parameter_value(p, "Comments"), 3) == "GND":
        val = "GND"
    elif left(get_parameter_value(p, "Comments"), 4) == "DATA":
        val = "DATA"
    elif left(get_parameter_value(p, "Comments"), 7) == "TELECOM":
        val = "TELECOM"
    elif left(get_parameter_value(p, "Comments"), 4) == "TEMP":
        val = "TEMP"
    else:
        val = "Branch"

    changed += set_parameter_value_by_name(p, "Conduit Use", val)


#t.Commit()
print(f'Changed: {changed}')
'''
