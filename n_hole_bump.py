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
	sph_obj1 = doc.addObject('Part::Sphere', 'Sphere1')
	sph1_rad = random.randint(5,15)
	sph_obj1.Radius = sph1_rad
	sph1_placement_x = random.randint(100,150)
	sph1_placement_y = random.randint(150,240)
	sph_obj1.Placement = App.Placement(App.Vector(sph1_placement_x,sph1_placement_y,2),App.Rotation(App.Vector(0,0,0),0))    # sph2_rad = random.randint(5,15)
	sph_obj1.Angle1 = 0 # For Bump
	add_obj = doc.addObject("Part::Fuse","fusion1")
	add_obj.Base = doc.Cut
	add_obj.Tool = doc.Sphere1
	Gui.ActiveDocument.setEdit('Sphere1',0)
	add_fillet = doc.addObject("Part::Fillet","Fillet1")
	add_fillet.Base = doc.fusion1
	__fillets__ = []
	__fillets__.append((11,1.00,1.00))
	add_fillet.Edges = __fillets__
	del __fillets__
    # sph2_placement_x = random.randint(130,150)
    # sph2_placement_y = random.randint(140,180)
    # sphere2 = Part.makeSphere(sph2_rad,50,Base.Vector(sph2_placement_x,sph2_placement_y,-5),Base.Vector(0,0,1))
	#Display
	import FreeCADGui
	FreeCADGui.ActiveDocument.activeView().viewAxonometric()
	FreeCADGui.SendMsgToActiveView("ViewFit")
	Gui.SendMsgToActiveView("Save")
	App.getDocument("test" + str(i)).save()
	# App.closeDocument("test" + str(i))
	# App.getDocument("test" + str(i)).saveAs(u"D:/Sudhir/MTP/FreeCAD/data" + "/test" + str(i) + ".FCStd")

	#Export to STL