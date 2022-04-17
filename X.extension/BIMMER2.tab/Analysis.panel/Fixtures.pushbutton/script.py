#! python3

from init0 import *
from toolz.curried import pipe, map, filter, reduce, valmap
from revito import *
from timeit import default_timer as timer
from general_funcs import iff
import random
import collections
import pandas as pd
import numpy as np
import math
#%matplotlib inline

from pyrevit import output


def is_number(x):
    return iff(type(x) == float or type(x) == int, True, False)

def number_check(x):
    return iff(type(x) == float or type(x) == int, x, 0)

def twfu(cwfu, hwfu):
    if cwfu == 0:
        return hwfu
    elif hwfu == 0:
        return cwfu
    else:
        return (0.7 * cwfu) + (0.7 * hwfu)
#from revit_common import *
#reload(revit_common)
#from revit_common import *


time_start = timer()

#get fixtures and specialty equipment
try:
    #all_picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")
    picks = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select something.")

except:
    pass

'''
items = pipe(   picks,
                map(lambda x: doc.GetElement(x)),
                filter(lambda x: x.Category.Name == "Plumbing Fixtures" or x.Category.Name == "Specialty Equipment"),
                tuple)
'''

items2 = pipe(   picks,
                map(lambda x: doc.GetElement(x)),
                filter(lambda x: x.Category.Name == "Plumbing Fixtures" or x.Category.Name == "Specialty Equipment"),
                map(lambda x: {   "WFU": number_check(get_parameter_value(get_family_type(x), "WFU")),
                                    "CWFU": number_check(get_parameter_value(get_family_type(x), "CWFU")),
                                    "HWFU": number_check(get_parameter_value(get_family_type(x), "HWFU")),
                                    "TWFU": twfu(number_check(get_parameter_value(get_family_type(x), "CWFU")), number_check(get_parameter_value(get_family_type(x), "HWFU"))),
                                     "MC-gph": number_check(get_parameter_value(get_family_type(x), "MC-gph")),
                                     "MC-flow": number_check(get_parameter_value(get_family_type(x), "MC-flow")),
                                     "MC-outlet_temperature": number_check(get_parameter_value(get_family_type(x), "MC-outlet_temperature"))} ),
                tuple)


#for i in items:
    #print(doc.GetElement(pick).Category.Name)
#    print(i.Category.Name)
#    print(get_parameter_value(get_family_type(i), "WFU"))


#dict1["key1"] = value1
def hunter_totals(d1, d2):
    d3 = {}
    d3["WFU"] = d1["WFU"] + d2["WFU"]
    d3["CWFU"] = d1["CWFU"] + d2["CWFU"]
    d3["HWFU"] = d1["HWFU"] + d2["HWFU"]
    d3["TWFU"] = d1["TWFU"] + d2["TWFU"]
    return d3

def dict_totals1(d1, d2):
    d3 = {}
    d3["flow_"] = d1["flow_"] + d2["flow_"]
    d3["flow_cw"] = d1["flow_cw"] + d2["flow_cw"]
    d3["flow_hw"] = d1["flow_hw"] + d2["flow_hw"]
    return d3


print(f'Items: {len(items2)}')
FUs = pipe( items2,
            reduce(hunter_totals),
            valmap(round))
print(FUs)


def monte_carlo(x):
    cw_temp = 50
    hw_temp = 140

    peak_gpm = x["MC-flow"]
    #print(f'peak_gpm: {iff(peak_gpm > 0, "adsfd", "zzzz")}')
    ave_gph = x["MC-gph"]

    if x["MC-outlet_temperature"] < cw_temp:
        mixed_temp = cw_temp
    elif x["MC-outlet_temperature"] > hw_temp:
        mixed_temp = hw_temp
    else:
        mixed_temp = x["MC-outlet_temperature"]

    hw_pct = (mixed_temp - cw_temp) / (hw_temp - cw_temp)
    cw_pct = 1 - hw_pct

    r = random.random()

    #chance_on = iff(peak_gpm > 0, (lambda a,b: (a / b) / 60)(ave_gph, peak_gpm), 0)
    if peak_gpm > 0:
        chance_on = (ave_gph / peak_gpm) / 60
    else:
        chance_on = 0

    flow_ = iff(chance_on > r, 1, 0) * peak_gpm
    if cw_pct> 1:
        print(f'{mixed_temp} {cw_pct} {hw_pct}')

    flows = {"flow_": flow_, "flow_cw": flow_ * cw_pct, "flow_hw" : flow_ * hw_pct}
    return flows
    #return flows


flow_connected = pipe(  items2,
                        map(lambda x: x["MC-flow"]),
                        sum)

print(f'total connected flow: {flow_connected}')

#map(function, iterable_list)

'''
flows = []
N = 1000
for n in range(N):
    flows.append(pipe(items2, map(monte_carlo), sum, round))
    #flows.append(pipe(items2, map(monte_carlo), reduce(dict_totals), valmap(round)))
'''

#print(pipe(items2, map(monte_carlo), reduce(dict_totals), valmap(round))
N=1000
#pipe(items2, map(monte_carlo), reduce(dict_totals1), valmap(round))
flows = pipe(range(N), map(lambda x: pipe(items2, map(monte_carlo), reduce(dict_totals1), valmap(round))), tuple)
#print(flows)
#flows = []
#N = 1000
#for n in range(N):
    #flows.append(pipe(items2, map(monte_carlo), reduce(dict_totals), valmap(round)))

#print(flows[100]["flow_"])
flows_ = pipe(flows, map(lambda x: x["flow_"]), tuple)
flows_cw = pipe(flows, map(lambda x: x["flow_cw"]), tuple)
flows_hw = pipe(flows, map(lambda x: x["flow_hw"]), tuple)

#print(f'highest flow: {max(flows)}')
print(f'Peak flow: {math.floor(np.percentile(flows_, 99))} gpm')
print(f'Peak cw flow: {math.floor(np.percentile(flows_cw, 99))} gpm')
print(f'Peak hw flow: {math.floor(np.percentile(flows_hw, 99))} gpm')
print(f'Average hw use: {math.floor(np.percentile(flows_hw, 50))} gpm ({math.floor(60 * np.percentile(flows_hw, 50))} gph)')


time_stop = timer()

print(f'Elapsed time: {round(time_stop - time_start, 1)}')
