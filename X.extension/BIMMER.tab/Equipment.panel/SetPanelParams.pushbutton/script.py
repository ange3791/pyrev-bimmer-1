#! python3

from init0 import *
import revito as rvt
from pyrevit import output


out = output.get_output()
out.close()


panel = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select panel."))
mark = rvt.get_parameter_value(panel, "Mark")

panel_tags = ["Front Model Text Value", "Top Model Text Value", "Front Model Text Value", "Panel Name"]

t = DB.Transaction(doc, 'Set panel name tags to match Mark')
t.Start()

for panel_tag in panel_tags:
    rvt.set_parameter_value_by_name(panel, panel_tag, mark)


t.Commit()
