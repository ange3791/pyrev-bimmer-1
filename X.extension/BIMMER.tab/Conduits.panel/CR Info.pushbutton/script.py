#! python3


#import init0
#reload(init0)
from init0 import *

import revito as rvt
from importlib import reload
reload(rvt)


from toolz.curried import pipe, map, filter
#from general_funcs import *

sel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))

cr_id = sel.RunId
cr = doc.GetElement(cr_id)
comments = rvt.get_parameter_value(cr, "Comments")
size = round(12 * rvt.get_parameter_value(cr, "Diameter(Trade Size)"), 3)
length1 = round(rvt.get_parameter_value(cr, "Length"))
type1 = rvt.get_parameter_value(doc.GetElement(rvt.get_parameter_value(cr, "Type")), "Type Name")


p_TO = rvt.get_parameter_value(cr, "TO")
p_FR = rvt.get_parameter_value(cr, "FR")
p_FDR = rvt.get_parameter_value(cr, "FDR")
p_PanelName = rvt.get_parameter_value(cr, "Panel Name")

#conduits = rvt.connected(sel, set(), 0)
conduits = rvt.connected(sel, set())
length2 = pipe(conduits, map(lambda x: rvt.conduit_length(doc.GetElement(x))), sum, round)


print(f'Conduit Run Id: {cr_id.IntegerValue}')
print(f'Comments: {comments}')
print(f'FR: {p_FR}')
print(f'TO: {p_TO}')
print(f'FDR: {p_FDR}')
print(f'Panel Name: {p_PanelName}')
print(f'Size: {size} in')
print(f'Type: {type1}')
print(f'Length: {length1} ft')

print(f'Length (connected method): {length2} ft')



params = cr.Parameters
for p in params:
    print(f'{p.Definition.Name}: {rvt.parameter_value(p)}')
