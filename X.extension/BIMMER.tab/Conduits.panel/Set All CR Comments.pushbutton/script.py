#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter
from timeit import default_timer as timer


time_start = timer()

conduit_pipes = pipe(   DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(), tuple)
conduit_fittings = pipe(   DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ConduitFitting).WhereElementIsNotElementType().ToElements(), tuple)
conduits = conduit_pipes + conduit_fittings


print(f'Conduits: {len(conduits)}')
#print(len(conduit_fittings))


changed = 0

t = DB.Transaction(doc, 'Set comments in conduit run')
t.Start()

for c in conduits:
    #changed += set_parameter_value_by_name(c, "Comments_tmp",
    comments = rvt.generate_Comments(   rvt.get_parameter_value(c, "Conduit Use"),
                                        rvt.get_parameter_value(c, "PANEL NAME"),
                                        rvt.get_parameter_value(c, "FDR"),
                                        rvt.get_parameter_value(c, "Extra"))
    #print(comments)
    changed += rvt.set_parameter_value_by_name(c, "Comments_tmp", comments)
    #changed += set_parameter_value_by_name(c, "Comments", comments)

t.Commit()

print(f'Changed: {changed}')
time_stop = timer()
print(f'Elapsed time: {round(time_stop - time_start, 1)}')
