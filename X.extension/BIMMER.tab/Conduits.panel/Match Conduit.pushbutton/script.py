#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter
#from general_funcs import *

sel1 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))
params = ["Conduit Use", "FDR", "FR", "TO", "PANEL NAME", "Extra", "Phase Breakdown", "Comments"]
#param_values = pipe(params, map(lambda x: tuple([x, rvt.get_parameter_value(sel1, x)])), dict)
param_values = pipe(    params,
                        filter(lambda x: rvt.get_parameter_value(sel1, x) is not None),
                        map(lambda x: tuple([x, rvt.get_parameter_value(sel1, x)])), dict)

go1 = True
while go1:
    try:
        sel2 = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

        changed = 0
        t = DB.Transaction(doc, 'Match params')
        t.Start()

        c = sel2
        for k, v in param_values.items():
            #print(f'{k} =  {v}')
            changed += rvt.set_parameter_value_by_name(c, k, v)

        t.Commit()

    except:
        go1 = False
        #print("bad")
