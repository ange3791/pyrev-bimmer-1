#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter


#get hangers
trapezes = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc, uidoc.ActiveView.Id), DB.BuiltInCategory.OST_ElectricalFixtures, "ElementIsNotType"),
                filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "MCE HANGER"),
                tuple)

print(f'Trapezes in this View={len(trapezes)}')


#set Top of Strut 1 to Offset
print('Setting Strut 1 Offset...')
t1 = DB.Transaction(doc, 'Set Top of Strut 1 = Offset')
t1.Start()
changed = list(map(lambda x: rvt.set_parameter_value_by_name(x, "Top of Strut 1", rvt.get_parameter_value(x, "Offset")), trapezes))
print(f'Changed: {len(list(filter(lambda x: x == 1, changed)))}')
t1.Commit()


#set config key for grouping
print('Setting hanger config key for schedule grouping...')

t1 = DB.Transaction(doc, 'Set trapeze schedule grouping parameter')
t1.Start()
param_names = ["Offset", "Primary Strut Length", "Rod Height 1", "Rod Height 2", "Strut 2", "Strut 2 Height"]
for el in trapezes:
    v = ''.join(map(lambda a: a + "=" + str(rvt.get_parameter_value(el, a)), param_names))
    x = abs(hash(v) % (10 ** 8))
    rvt.set_parameter_value_by_name(el, "HangerConfigKey", int(x))
t1.Commit()

#get single strut hangers
hanger_configs_1strut = pipe(trapezes,
                          filter(lambda x: rvt.get_parameter_value(x.Symbol, "Strut 1") == True and rvt.get_parameter_value(x.Symbol, "Strut 2") == None and rvt.get_parameter_value(x.Symbol, "Strut 3") == None and rvt.get_parameter_value(x.Symbol, "Strut 4") == None),
                          map(lambda x: rvt.get_parameter_value(x, "HangerConfigKey")),
                          set,
                          sorted,
                          tuple)

#print(len(hanger_configs_1strut))
print(f'Single Strut hangers: {len(set(hanger_configs_1strut))}')

#renumber Item Numbers
print('Setting Single Strut HangerConfigKey...')
t1 = DB.Transaction(doc, 'Set trapeze Item Numbers')
t1.Start()
prefix = ""
n=100
for hanger_config in hanger_configs_1strut:
    n+=1
    #print(hanger_config)
    traps = pipe(trapezes, filter(lambda x: rvt.get_parameter_value(x, "HangerConfigKey") == hanger_config), tuple)
    #print(len(traps))
    x1 = list(map(lambda x: rvt.set_parameter_value_by_name(x, "Item Number", prefix + str(n)), traps))
    #print(sum(x1))
t1.Commit()
