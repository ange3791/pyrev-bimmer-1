#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap
import revito as rvt
from general_funcs import iff

#from pyrevit import output

#get fixtures and specialty equipment
#try:
    #all_picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")
    #picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")

#except:
#    pass

#import Autodesk.Revit as AR
#print(AR.ApplicationServices.Application.BackgroundColor)
#print(DB.ColorOptions.BackgroundColor.GetValue)
#print("sdfsdf")


try:
    sel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select something."))
    #param_values = pipe(params, map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)
    #param_values = pipe(    params,
    #                        filter(lambda x: rvt.get_parameter_value(sel, x) is not None),
    #                        map(lambda x: tuple([x, rvt.get_parameter_value(sel, x)])), dict)

except:
    sel = None



#def connected_to(conn):
#    return pipe(conn.AllRefs, filter(lambda x: conn.Owner.Id != x.Owner.Id), map(lambda x: x.Owner), tuple)

#for c in connector.AllRefs:
#    print(f'___   {c.Owner.Id}')

print(f'Id: {sel.Id}')

if sel.Category.Name == "Pipes":
    all_connectors = sel.ConnectorManager.Connectors
elif sel.Category.Name == "Pipe Fittings":
    all_connectors = sel.MEPModel.ConnectorManager.Connectors

count = 0
connectors = pipe(  all_connectors,
                    filter(lambda x: x.ConnectorType !=32),
                    tuple)

count = count + len(connectors)
print(f'count: {count}')

for connector in connectors:
    print(f'Connecter: {connector}')
    if connector.IsConnected == True:
        #for c in connector.AllRefs:
        #    print(f'___   {c.Owner.Id}')
        for c in connected_to(connector):
            print(c.Id)

#    if (connector.ConnectorType != 32) and (connector.IsConnected == True):
#        connector_set = connector.AllRefs
#        for c in connector_set:



#print(count)
#connectors = el.MEPModel.ConnectorManager.Connectors
#if sel is not None:
#    pipes = rvt.connected(sel, set(), 0)

#print(len(pipes))
