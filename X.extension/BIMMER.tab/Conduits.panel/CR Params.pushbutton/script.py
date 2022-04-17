#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter
#from pyrevit import output
#from general_funcs import *

#out = output.get_output()
#out.close()

params = ["Conduit Use", "FDR", "FR", "TO", "Extra", "Phase Breakdown", "PANEL NAME", "Comments"]
changed = 0



try:
    sel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))
    #param_values = pipe(params, map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)
    param_values = pipe(    params,
                            filter(lambda x: rvt.get_parameter_value(sel, x) != None),
                            map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)

except:
    sel = None

#Is Conduit Use defined
ConduitUse = "Conduit Use" in list(param_values.keys())


if sel is not None:
    conduits = rvt.connected(sel, set())
    #print(f'Connected: {len(conduits)}')

    t = DB.Transaction(doc, 'Match params in conduit run')
    t.Start()

    for c_id in conduits:
        c = doc.GetElement(c_id)

        for k, v in param_values.items():
            #print(f'{k} =  {v}')
            if k == "Comments" and ConduitUse:
                #Generat Comments from custom params
                changed += rvt.set_parameter_value_by_name(c, "Comments", rvt.generate_Comments(param_values['Conduit Use'], param_values['PANEL NAME'], param_values['FDR'], param_values['Extra']))
            else:
                changed += rvt.set_parameter_value_by_name(c, k, v)

        #changed += set_parameter_value_by_name(c, "PANEL NAME", param_values['FR'])
        #changed += rvt.set_parameter_value_by_name(c, "Comments_tmp", rvt.generate_Comments(param_values['Conduit Use'], param_values['PANEL NAME'], param_values['FDR'], param_values['Extra']))
        #changed += rvt.set_parameter_value_by_name(c, "Comments", rvt.generate_Comments(param_values['Conduit Use'], param_values['PANEL NAME'], param_values['FDR'], param_values['Extra']))
    
    t.Commit()
