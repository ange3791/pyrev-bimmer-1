#! python3

from init0 import *
from toolz.curried import pipe, map, filter
from revito import *
from timeit import default_timer as timer
#from general_funcs import *


#from revit_common import *
#reload(revit_common)
#from revit_common import *


time_start = timer()



conduit_pipes = pipe(   DB.FilteredElementCollector(doc, uidoc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements(),
                        map(lambda x: tuple([
                                                x,
                                                x.RunId.IntegerValue,
                                                get_parameter_value(x, "Comments")
                                                ])),
                                                tuple)

#get conduit runs in view
conduit_runs0 = pipe(   conduit_pipes,
                        map(lambda x: x[1]),
                        set,
                        tuple)

#            filter(lambda x: x.Id.IntegerValue in conduit_runs0),

conduit_runs1 = pipe(  DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ConduitRun).WhereElementIsNotElementType().ToElements(),
            filter(lambda x: get_parameter_value(x, "Type") is not None),
            map(lambda x:
                [   x.Id.IntegerValue,
                    get_parameter_value(x, "Comments"),
                    str(round(12 * get_parameter_value(x, "Diameter(Trade Size)"), 3)),
                    get_parameter_value(doc.GetElement(get_parameter_value(x, "Type")), "Type Name"),
                    round(get_parameter_value(x, "Length"), 1),
                    ]),
             tuple)


print(len(conduit_runs1))

#get conduit runs with no Comments
crX = pipe( conduit_runs1,
            filter(lambda x: x[1] == ""),
            tuple)

for conduit_run in crX:
    print(f'Conduit Run: {conduit_run[0]}: {conduit_run[1]}')
    #pipes_in_run = pipe(conduit_pipes, filter(lambda x: x[1] == conduit_run[0]))
    pipes_in_run = pipe(conduit_pipes, filter(lambda x: x[1] == conduit_run[0]), tuple)
    if len(pipes_in_run) > 0:
        #get all connected in run
        #print(f'___{get_parameter_value(pipes_in_run[0][0], "Length")}')
        conduits_in_run = connected(pipes_in_run[0][0], set(), 0)
        #print(len(conduits_in_run))
        for c_id in conduits_in_run:
            c = doc.GetElement(c_id)
            print(f'___id: {c_id}, Comments: {get_parameter_value(c, "Comments")}, FDR: {get_parameter_value(c, "FDR")}, FR: {get_parameter_value(c, "FR")}')


print(len(crX))


time_stop = timer()

print(f'Elapsed time: {round(time_stop - time_start, 1)}')
