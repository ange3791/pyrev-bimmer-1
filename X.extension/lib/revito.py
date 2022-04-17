from general_funcs import conc, list_diff
from toolz.curried import pipe, map, filter, reduce


def all_elements_of_category(collector, category, ElementIs):
    if ElementIs == "ElementType":
        return collector.OfCategory(category).WhereElementIsElementType().ToElements()
    else:
        return collector.OfCategory(category).WhereElementIsNotElementType().ToElements()


def generate_Comments(x0, panel_name, fdr_number, extra):
    if x0 == "Branch":
        a1 = panel_name
        sep = " - "
    else:
        a1 = x0
        sep = " "

    if extra is not None and len(extra) > 0:
        a2 = conc(" ", extra)
    else:
        a2 = ""

    return conc(a1, sep, fdr_number, a2).strip()


def conduit_length(item):
    if item.Category.Name == "Conduits":
        #conduit pipe
        return get_parameter_value(item, "Length")
    else:
        #fitting
        if get_parameter_value(item, "Bend Radius") is not None:
            s = get_parameter_value(item, "Angle") * get_parameter_value(item, "Bend Radius")
            l = get_parameter_value(item, "Conduit Length")
            return s + (2 * l)
        else:
            return 0

def conduit_size(x):
    if x.Category.Name == "Conduits":
        return round(12 * get_parameter_value(x, "Diameter(Trade Size)"), 3)

    else:
        #fitting
        s = get_parameter_value(x, "Nominal Diameter")
        if s is not None:
            return round(12 * s, 3)
        else:
            return 0


def get_parameter_object_by_name(el, parameter_name):
    try:
        x = el.GetParameters(parameter_name)[0]
    except:
        x = 0
        pass

    return x


def get_parameter_value(el, parameter_name):

    if len(el.GetParameters(parameter_name)) > 0:
    	return parameter_value(el.GetParameters(parameter_name)[0])

    else:
        return None


def set_parameter_value_by_name(el, parameter_name, new_value):
    #category = el.Category.Name
    #if category == "Conduits" or category == "Conduit Fittings":
    param_object = get_parameter_object_by_name(el, parameter_name)

    old_value = parameter_value(param_object)
    #new_value = value
    '''
    if type(value) == float:
        old_value = round(parameter_value(param_object), 7)
        new_value = round(value, 7)

    else:
        old_value = parameter_value(param_object)
        new_value = value
    '''
    #print(f'changing: {old_value}, {value}')
    #print(f'changing: {conc("|", old_value, "|")} {conc("|", new_value, "|")}')
    if new_value != old_value:
        param_object.Set(new_value)
        return 1

    else:
        return 0


def parameter_value(parameter):
    #storage_type["Double"] =
    storage_types = dict(Integer=1, Double=2, String=3, ElementId=4)
    x = parameter.StorageType

    #print(f'StorageType={x}')
    #if x == storage_types.Double:
    #print(f'{parameter} : {parameter.HasValue}')

    if parameter.HasValue:
        if x == storage_types["Double"]:
            value = parameter.AsDouble()
            #value = parameter.AsValueString()

        elif x == storage_types["Integer"]:
            value = parameter.AsInteger()
            #value = param.AsInteger().ToString()

        elif x == storage_types["String"]:
            value = parameter.AsString()

        elif x == storage_types["ElementId"]:
            value = parameter.AsElementId()
            #value = document.GetElement(param.AsElementId()).Name

        else:
            value = None

    else:
        value = None

    return value


def get_family_name(x):
    return get_family_type(x).FamilyName
    #element_id = x.GetTypeId()
    #element_type = x.Document.GetElement(element_id)
    #return element_type.FamilyName

def get_family_type(x):
    element_id = x.GetTypeId()
    return x.Document.GetElement(element_id)
    #return element_type.FamilyName

def get_family_type_name(x):
    #element_id = x.GetTypeId()
    #element_type = x.Document.GetElement(element_id)
    #return element_type
    return x.Name


def connected_to_connector(conn):
    return pipe(conn.AllRefs, filter(lambda x: x.Owner.Id != conn.Owner.Id), tuple)[0]


def connected_to(x):

    if x.Category.Name == "Pipes" or x.Category.Name == "Conduits":
        #return connector for pipes / conduits
        all_connectors = x.ConnectorManager.Connectors

    else:
        try:
            #return connector for fitting / family instance 
            all_connectors = x.MEPModel.ConnectorManager.Connectors
        except:
            pass

    connectors = pipe(  all_connectors,
                    #filter(lambda x: x.ConnectorType != 32 and x.IsConnected),
                    filter(lambda x: x.ConnectorType != 32 and x.IsConnected),
                    tuple)

    l1 = list()
    for conn in connectors:
        l1.append(connected_to_connector(conn).Owner)

    return tuple(l1)


def connected(el, running):
    #return connected
    running.add(el.Id)

    #for ct in connected_to(el):
    for ct in pipe(connected_to(el), filter(lambda x: x.Id not in running), tuple):
        #if ct.Id not in running:
        connected(ct, running)

    return running



def connected_old(el, running, count):
    #return connected conduits
    running.add(el.Id)

    try:
        #return connector for conduit
        connectors = el.ConnectorManager.Connectors
    except:
        pass

    try:
        #return connector for family instance
        connectors = el.MEPModel.ConnectorManager.Connectors
    except:
        #print("not fitting")
        pass

    for conn in connectors:
        if conn.ConnectorType != 32:
            count += 1
    #count += len(connectors)
    #count += connectors.Size

    for connector in connectors:

        if (connector.ConnectorType != 32) and (connector.IsConnected == True):
            connector_set = connector.AllRefs
            for c in connector_set:
                #if connector.ConnectorType == DB.ConnectorType.Physical and c.Owner.Id not in running:
                if c.Owner.Id not in running:
                    connected_old(c.Owner, running, count)

        count -= 1
        if count == 0:
            return running



def connected_0(el, running):
    #return connected
    running.add(el.Id)

    for ct in connected_to(el):

        if ct.Id not in running:
            connected_0(ct, running)

    return running



def connectors_connected_to(conn):
    return pipe(conn.AllRefs, filter(lambda x: x.Owner.Id != conn.Owner.Id), tuple)


def get_pipe_ends(p):
    return (p.Location.Curve.GetEndPoint(0), p.Location.Curve.GetEndPoint(1))

def get_closest_connectors(pipeA, pipeB):
    #pipeA_connectors = pipe(pipeA.ConnectorManager.Connectors, tuple)
    pipeA_connectors = pipeA.ConnectorManager.Connectors
    #pipeB_connectors = pipe(pipeB.ConnectorManager.Connectors, tuple)
    pipeB_connectors = pipeB.ConnectorManager.Connectors
    l1 = list()
    for connA in pipeA_connectors:
        for connB in pipeB_connectors:
            l1.append([connA.Origin.DistanceTo(connB.Origin), connA, connB])

    min0 = min(l1)
    return (min0[1], min0[2])


def get_pipe_PipingSystemTypeId(pipe):
    return pipe.MEPSystem.GetTypeId()
    #return pipe.MEPSystem

def get_pipe_PipeType(pipe):
    return pipe.PipeType

def get_pipe_Level(pipe):
    return pipe.ReferenceLevel
    #doc.ActiveView.GenLevel.Id
