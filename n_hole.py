i = 1
for i in range(1):
	doc = App.newDocument("test" + str(i))
	App.setActiveDocument("test" + str(i))
	App.ActiveDocument=App.getDocument("test" + str(i))
	Gui.ActiveDocument=Gui.getDocument("test" + str(i))
	# Save Model
	App.getDocument("test" + str(i)).saveAs(u"D:/Sudhir/MTP/FreeCAD/data" + "/test" + str(i) + ".FCStd")
	# part
	import Part
	box_obj = doc.addObject('Part::Box', 'Box')
	box_obj.Height = 2
	box_obj.Width = 300
	box_obj.Length = 1000
	cyl_obj = doc.addObject('Part::Cylinder', 'Cylinder')
	cyl_obj.Height = 50
	import random
	cyl_radius = random.randint(10, 58) 
	cyl_obj.Radius = cyl_radius
	cyl_placement_x = random.randint(62, 240)
	cyl_placement_y = random.randint(62, 240)
	# cyl_obj.Placement = App.Placement(App.Vector(300,0,0),App.Rotation(App.Vector(0,0,1),0))
	cyl_obj.Placement = App.Placement(App.Vector(cyl_placement_x,cyl_placement_y,-5),App.Rotation(App.Vector(0,0,1),0))
	# cyl_obj.Placement =
	cut_obj = doc.addObject("Part::Cut","Cut")
	cut_obj.Base = doc.Box
	cut_obj.Tool = doc.Cylinder
	Gui.ActiveDocument.setEdit('Cut',0)
	#Display
	import FreeCADGui
	FreeCADGui.ActiveDocument.activeView().viewAxonometric()
	FreeCADGui.SendMsgToActiveView("ViewFit")
	Gui.SendMsgToActiveView("Save")
	App.getDocument("test" + str(i)).save()
	# App.closeDocument("test" + str(i))
	# App.getDocument("test" + str(i)).saveAs(u"D:/Sudhir/MTP/FreeCAD/data" + "/test" + str(i) + ".FCStd")

	#Export to STL