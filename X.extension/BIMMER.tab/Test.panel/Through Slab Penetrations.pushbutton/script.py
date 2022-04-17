#! python3

from init0 import *
from toolz.curried import pipe, map, filter
import revito as rvt
from general_funcs import between, list_count, strfind
#from general_funcs import *

#el = doc.GetElement(uidoc.Selection.PickObject(Selection.ObjectType.Element, 'Choose element'))
#print(el.Symbol.FamilyName)

#get the active view
view = uidoc.ActiveView

#get level of view
level = view.GenLevel
level_elevation = level.Elevation

'''
level_ = pipe(  DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Level).WhereElementIsNotElementType().ToElements(),
                filter(lambda x: strfind("BOS", rvt.get_parameter_value(x, "DOCTAG")),
                filter(lambda x: rvt.get_parameter_value(x, "Elevation") < level_elevation),
                map(lambda x: [x, rvt.get_parameter_value(x, "Elevation")]),
                lambda x: sorted(x, key=lambda y: y[1]),
                lambda x: x[:1])
'''



#print(level_[1])
floor_thickness = 5.5/12
print(f'Top of floor: {level.Elevation}')
print(f'Bottom of floor: {level.Elevation - floor_thickness}')


def fitting_points(fitting):
    connectors = fitting.MEPModel.ConnectorManager.Connectors
    #print(len(connectors))
    cn = list()
    for connector in connectors:
        cn.append(connector.Origin)

    return cn

#does pipe penetrate floor?
'''
def pipe_through_floor(elevation, pipe1):
    y_start  = pipe1.Location.Curve.GetEndPoint(0)[2]
    y_end  = pipe1.Location.Curve.GetEndPoint(1)[2]
    return between(elevation, y_start, y_end)


#does fitting penetrate floor?
def fitting_through_floor(elevation, fitting):
    points = fitting_points(fitting)
    #print(points)
    if len(points) == 2:
        return between(elevation, points[0][2], points[1][2])
    else:
        return False
'''

def conduit_endpoints(c):

    if c.Category.Name == "Conduits":
        #is conduit
        points = sorted([c.Location.Curve.GetEndPoint(0)[2], c.Location.Curve.GetEndPoint(1)[2]])

    else:
        #is fitting
        p_ = fitting_points(c)
        if len(p_) != 2:
            points = None

        else:
            points = sorted([p_[0][2], p_[1][2]])

    return points


def conduit_through_floor(pipe1, floor_bottom, floor_top):

    points = conduit_endpoints(pipe1)
    if points is None:
        return False
    else:
        y_low = points[0]
        y_high = points[1]
        #print(f'{floor_bottom} {floor_top}')

        return y_low < floor_bottom and y_high > floor_top


def conduit_through_top(pipe1, floor_bottom, floor_top):

    points = conduit_endpoints(pipe1)
    if points is None:
        return False
    else:
        y_low = points[0]
        y_high = points[1]

        return between(floor_top, y_low, y_high) and y_low > floor_bottom


def conduit_through_bottom(pipe1, floor_bottom, floor_top):

    points = conduit_endpoints(pipe1)
    if points is None:
        return False
    else:
        y_low = points[0]
        y_high = points[1]

        return between(floor_bottom, y_low, y_high) and y_high < floor_top



#get counduits passing through floor
conduit_pipes = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc), DB.BuiltInCategory.OST_Conduit, "ElementIsNotType"), tuple)

#get conduit fittings passing through floor
conduit_fittings = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc), DB.BuiltInCategory.OST_ConduitFitting, "ElementIsNotType"), tuple)

conduits = conduit_pipes + conduit_fittings
print(f'Conduits: {len(conduits)}')

c_through = pipe(   conduits,
                    filter(lambda x: conduit_through_floor(x, level.Elevation - floor_thickness, level.Elevation)),
                    tuple)

c_through_top = pipe(   conduits,
                        filter(lambda x: conduit_through_top(x, level.Elevation - floor_thickness, level.Elevation)),
                        tuple)

c_through_bottom = pipe(    conduits,
                            filter(lambda x: conduit_through_bottom(x, level.Elevation - floor_thickness, level.Elevation)),
                            tuple)

print(f'Conduit Through Floor: {len(c_through)}')
print(f'Conduit Through Floor Top only: {len(c_through_top)}')
print(f'Conduit Through Floor Bottom only: {len(c_through_bottom)}')


#pipe_penetrations(floor, through


'''
counter = 0
for p in pipes_through_floor:
    point = DB.XYZ(p.Location.Curve.GetEndPoint(0)[0], p.Location.Curve.GetEndPoint(0)[1], float(0))
        counter += 1


for ftg in fittings_through_floor:
    points = tuple(fitting_points(ftg))
    fitting_top = sorted(points, key = lambda x: x[2])[1]
    #print(fitting_top)
    point = DB.XYZ(fitting_top[0], fitting_top[1], float(0))
        counter += 1
'''

#print(f'Added: {counter}')
#BoundingBoxContainsPointFilter() = elements that have a bb that contains the given point
#BoundingBoxIntersectsFilter() = elements that have a bb that intersects a given outline
#BoundingBoxIsInsideFilter(outline) = elements that have a bounding box inside a given outline
