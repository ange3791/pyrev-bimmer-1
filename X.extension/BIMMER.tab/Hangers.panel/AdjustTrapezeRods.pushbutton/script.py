#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter
from math import sin, cos, floor, modf
from general_funcs import round_to


#NEEDS A 3D VIEW!!!!
#get current view
view = uidoc.ActiveView


def adjust_hanger_rods(el, reference_intersector):
    #get hanger location and rotation
    location = el.Location
    p0 = location.Point
    theta = location.Rotation

    #get rod base locations
    rod1_offset = rvt.get_parameter_value(el, "Rod 1 Offset")
    rod2_offset = rvt.get_parameter_value(el, "Rod 2 Offset")
    strut_length = rvt.get_parameter_value(el, "Primary Strut Length")
    p_rod1_base = DB.XYZ(p0.X + rod1_offset * cos(theta), p0.Y + rod1_offset * sin(theta), p0.Z)
    p_rod2_base = DB.XYZ(p0.X + (strut_length - rod2_offset) * cos(theta), p0.Y + (strut_length - rod2_offset) * sin(theta), p0.Z)
    #fix this
    rods = {'Rod Height 1': p_rod1_base, 'Rod Height 2': p_rod2_base}

    #ReferenceIntersector(ElementId, FindReferenceTarget, View3D)
    #ReferenceIntersector(View3D)
    #FindReferenceTarget options: Element, Mesh, Edge, Curve, Face or All.

    ray_direction = DB.XYZ(float(0), float(0), float(1))

    counter = 0
    for k, v in rods.items():
        #print(f'{k, v}')
        reference_with_context = reference_intersector.FindNearest(v, ray_direction)
        #print(reference_intersector.FindReferencesInRevitLinks)
        reference = reference_with_context.GetReference()
        p_above = reference.GlobalPoint
        rod_length = round_to(p_above.Z - v.Z, float(.5/12))
        #print(f'{k} Old={get_parameter_value(el, k)}, New={rod_length}')
        counter += rvt.set_parameter_value_by_name(el, k, rod_length)

    return counter

#trapezes = doc.GetElement(uidoc.Selection.PickObjects(Selection.ObjectType.Element, 'Choose elements'))
#sel = uidoc.Selection.PickObjects(Selection.ObjectType.Element, 'Choose elements')
#trapezes = pipe(sel, map(lambda x: doc.GetElement(x)), filter(lambda x: x.Category.Name == "Electrical Fixtures"), filter(lambda x: get_parameter_value(x.Symbol, "Family Name") == "MCE HANGER"), tuple)
##trapezes = pipe(sel, map(lambda x: doc.GetElement(x)), tuple)

#get all trapeze hangers in view
trapezes = pipe(rvt.all_elements_of_category(DB.FilteredElementCollector(doc, view.Id), DB.BuiltInCategory.OST_ElectricalFixtures, "ElementIsNotType"),
                    filter(lambda x: rvt.get_parameter_value(x.Symbol, "Family Name") == "MCE HANGER"),
                    tuple)

print(f'Trapezes={len(trapezes)}')

#filter1 = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_StructuralFraming)
#filter2 = DB.ElementClassFilter(getattr(DB, "FootPrintRoof"))
#filter3 = DB.ElementClassFilter(getattr(DB, "Floor"))
filter = DB.LogicalOrFilter(DB.LogicalOrFilter(DB.ElementClassFilter(getattr(DB, "FootPrintRoof")), DB.ElementClassFilter(getattr(DB, "Floor"))), DB.ElementCategoryFilter(DB.BuiltInCategory.OST_StructuralFraming))

reference_intersector1 = DB.ReferenceIntersector(filter, DB.FindReferenceTarget.Face, view)
#reference_intersector = DB.ReferenceIntersector(view)
reference_intersector1.FindReferencesInRevitLinks = True



t = DB.Transaction(doc, 'adjust rod length')
t.Start()
#i = 0
n = 0
for hanger in trapezes:
    #i += 1
    #print(hanger.Category.Name)
    #print(i)
    n += adjust_hanger_rods(hanger, reference_intersector1)

t.Commit()

print(f'Rod lengths changed: {n}')
