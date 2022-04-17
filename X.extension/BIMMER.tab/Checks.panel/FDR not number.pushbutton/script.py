#! python3

from init0 import *
from toolz.curried import pipe, map, filter
import revito as rvt


conduit_pipes = pipe(   DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(), tuple)
conduit_fittings = pipe(   DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ConduitFitting).WhereElementIsNotElementType().ToElements(), tuple)
conduits = conduit_pipes + conduit_fittings


print(len(conduit_pipes))
print(len(conduit_fittings))



changed = 0

#t = DB.Transaction(doc, 'Set comments in conduit run')
#t.Start()

for c in conduits:
    fdr = rvt.get_parameter_value(c, "FDR")
    if fdr is not None:
        s = fdr.split(" ")
        if len(s) > 1:
            print(f'FDR: {fdr}')
            print(f'___FR: {rvt.get_parameter_value(c, "FR")}')
            print(f'___TO: {rvt.get_parameter_value(c, "TO")}')
            print(f'___PANEL NAME: {rvt.get_parameter_value(c, "PANEL NAME")}')


    '''
    if fdr is not None:
        s = fdr.split(" ")
        if len(s) == 3 and s[1] == "-":
            if get_parameter_value(c, "FR") == s[0]:
                print(f'{s[2]}')
                #set_parameter_value_by_name(c, "FDR", s[2])

                #print(f'{s[2]}, {get_parameter_value(c, "FR")}, {get_parameter_value(c, "PANEL_NAME")} {x1}')
    '''

    '''
    if fdr is not None:
        s = fdr.split(" ")
        if len(s) == 2:
            if s[0] == "TEMP":
                ##print(f'{s}, {get_parameter_value(c, "Conduit Use")}')
                #print(f'{fdr}, FR: {get_parameter_value(c, "FR")}, PANEL: {get_parameter_value(c, "PANEL NAME")}, {get_parameter_value(c, "Conduit Use")}')
                #changed += set_parameter_value_by_name(c, "FDR", s[1])
                #changed += set_parameter_value_by_name(c, "Conduit Use", "TEMP")

    '''



    '''
    fdr0 = get_parameter_value(c, "FDR")
    fdr = iff(fdr0 is None, "", fdr0).lstrip("0")

    if get_parameter_value(c, "Conduit Use") == "Branch":
        x = conc(get_parameter_value(c, "FR"), " ", fdr)

    else:
        x = conc(get_parameter_value(c, "Conduit Use"), " ", fdr)

    print(x)
    '''
    #changed += set_parameter_value_by_name(c, "Comments_tmp", x)

#t.Commit()

print(f'Changed: {changed}')
