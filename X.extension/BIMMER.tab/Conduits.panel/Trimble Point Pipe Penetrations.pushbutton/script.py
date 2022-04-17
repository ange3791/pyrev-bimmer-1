#! python3

from init0 import *
from toolz.curried import pipe, map, filter
import revito as rvt
from general_funcs import between
#from general_funcs import *

#el = doc.GetElement(uidoc.Selection.PickObject(Selection.ObjectType.Element, 'Choose element'))
#print(el.Symbol.FamilyName)

#get the active view
view = uidoc.ActiveView

#get level of view
level = view.GenLevel
level_elevation = level.Elevation

print(f'Level elevation: {level.Elevation}')


def fitting_points(fitting):
    connectors = fitting.MEPModel.ConnectorManager.Connectors
    #print(len(connectors))
    cn = list()
    for connector in connectors:
        cn.append(connector.Origin)

    return cn

#does pipe penetrate floor?
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


#get counduits passing through floor
pipes_through_floor = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc, view.Id), DB.BuiltInCategory.OST_Conduit, "ElementIsNotType"),
                           filter(lambda x: pipe_through_floor(level_elevation, x)),
                           tuple)



#get conduit fittings passing through floor
fittings_through_floor = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc, view.Id), DB.BuiltInCategory.OST_ConduitFitting, "ElementIsNotType"),
                              filter(lambda x: fitting_through_floor(level_elevation, x)),
                              tuple)


def already_there(point, level_elevation):
    #fix this!!! needs to match against selected family...
    tol = .25
    outline_min = DB.XYZ(point[0] - tol, point[1] - tol, level_elevation - tol)
    outline_max = DB.XYZ(point[0] + tol, point[1] + tol, level_elevation + tol)
    outline = DB.Outline(outline_min, outline_max)
    filter1 = DB.BoundingBoxIsInsideFilter(outline)

    list1 =  pipe(   DB.FilteredElementCollector(doc).WherePasses(filter1).WhereElementIsNotElementType().ToElements(),
                    map(lambda x: "point" in rvt.get_parameter_value(x.Symbol, "Family Name").lower()),
                    tuple)
    if True in list1:
        return True
    else:
        return False


#get family to copy and place at penetrations
try:
    el = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, 'Pick control point to copy'))

except:
    print("Pick cancelled")
    el = None
    #print(el)
    pass


if el is not None:
    family_symbol = el.Symbol

    t = DB.Transaction(doc, 'Automatic control points for stub ups')
    t.Start()

    counter = 0
    for p in pipes_through_floor:
        point = DB.XYZ(p.Location.Curve.GetEndPoint(0)[0], p.Location.Curve.GetEndPoint(0)[1], float(0))
        if not already_there(point, level_elevation):
            doc.Create.NewFamilyInstance(point, family_symbol, level, DB.Structure.StructuralType.NonStructural)
            counter += 1


    for ftg in fittings_through_floor:
        points = tuple(fitting_points(ftg))
        fitting_top = sorted(points, key = lambda x: x[2])[1]
        #print(fitting_top)
        point = DB.XYZ(fitting_top[0], fitting_top[1], float(0))
        if not already_there(point, level_elevation):
            doc.Create.NewFamilyInstance(point, family_symbol, level, DB.Structure.StructuralType.NonStructural)
            counter += 1

    t.Commit()

print(f'Added: {counter}')
#BoundingBoxContainsPointFilter() = elements that have a bb that contains the given point
#BoundingBoxIntersectsFilter() = elements that have a bb that intersects a given outline
#BoundingBoxIsInsideFilter(outline) = elements that have a bounding box inside a given outline
