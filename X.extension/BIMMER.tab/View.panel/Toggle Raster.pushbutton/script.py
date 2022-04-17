#! python3

from init0 import *
import revito as rvt
from toolz.curried import pipe, map, filter

view = uidoc.ActiveView
raster_id = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_RasterImages).Id
raster_visible = view.GetCategoryHidden(raster_id)

t = DB.Transaction(doc, 'Change Raster visibility')
t.Start()
if view.IsCategoryOverridable(raster_id):
    view.SetCategoryHidden(raster_id, not raster_visible)

else:
    viewtemplate = doc.GetElement(view.ViewTemplateId)
    viewtemplate.SetCategoryHidden(raster_id, not raster_visible)

t.Commit()


#view = uidoc.ActiveView
#x = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Coordination_Model)
#print(x)


#coordination_model_id = DB.VIS_GRAPHICS_COORDINATION_MODEL
#DB.BuiltInCategory.OST_Coordination_Model


#print(raster_visible)
#print(not raster_visible)
#print(viewt.GetCategoryHidden(rasterimages.Id))

#print(viewt.GetCategoryHidden(raster))

#
#    viewtemplate.SetCategoryHidden(rasterimages.Id, False)

#for i in view.GetCategoryOverrides():


#for i in view.GetCategoryOverrides(raster_id):
#    print(i)

#for i in view.Document.Settings.Categories:
#    if "Raster" in i.Name:
#        print(f'{i.Id}: {i.Name}')
#        print(view.GetCategoryHidden(i.Id))
        #view.SetCategoryHidden(i.Id, False)
        #print(f'template id {')
        #
        #i.Visible = True
        #print(f'{i.Id}: {i.Name} Visible: {i.IsVisibleInUI}')

        #print(f'{i.Id}: {i.Name} Visible: {i.IsVisibleInUI}')

    #if "Raster" in i.Name:
    #    print(f'{i.Id}: {i.Name} Visible: ')

#t.Commit()



#os.sys.path = path1
#path1 = [   "C:\Users\ange3\Box\RevitX\MCE\PyRev\pyrevit_scripts\X.extension\BIMMER.tab\Test.panel\Test3.pushbutton",
#            "C:\Users\ange3\Box\RevitX\MCE\PyRev\pyrevit_scripts\X.extension\lib",
#            "C:\Users\ange3\AppData\Roaming\pyRevit-Master\pyrevitlib",
#            "C:\Users\ange3\AppData\Roaming\pyRevit-Master\site-packages",
#            "C:\Users\ange3\AppData\Local\Programs\Python\Python38\Lib\site-packages;",
#            "C:\Users\ange3\AppData\Roaming\pyRevit-Master\bin\engines\385\python38.zip",
#            "C:\Users\ange3\AppData\Roaming\pyRevit-Master\bin\engines\385",
#            "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\"]
