#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter
from pyrevit import output
#from general_funcs import *

#out = output.get_output()
#out.close()

#picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Picks")
#f1 = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Conduits)
#f2 = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_ConduitFitting)

try:
    all_picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")

except:
    pass

picks = pipe(   all_picks,
                filter(lambda x: doc.GetElement(x).Category.Name == "Conduits"),
                tuple)

#for p in picks:
    #print(p)
    #print(doc.GetElement(p).Category.Name)

if len(picks) > 0:
    changed = 0
    params = ["Conduit Use", "FDR", "FR", "TO", "Extra", "Phase Breakdown", "PANEL NAME"]

    t = DB.Transaction(doc, 'Match params in conduit run')
    t.Start()

    for pick in picks:
        sel = doc.GetElement(pick)
        param_values = pipe(params, map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)

        conduits = rvt.connected(sel, set())
        #print(f'Connected: {len(conduits)}')
        for c_id in conduits:
            c = doc.GetElement(c_id)

            for k, v in param_values.items():
                #print(f'{k} =  {v}')
                changed += rvt.set_parameter_value_by_name(c, k, v)

            #changed += rvt.set_parameter_value_by_name(c, "Comments_tmp", rvt.generate_Comments(param_values['Conduit Use'], param_values['FR'], param_values['FDR'], param_values['Extra']))
            changed += rvt.set_parameter_value_by_name(c, "Comments", rvt.generate_Comments(param_values['Conduit Use'], param_values['PANEL NAME'], param_values['FDR'], param_values['Extra']))

    t.Commit()
