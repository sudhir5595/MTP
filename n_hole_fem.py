i = 2
for i in range(2):
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
	App.closeDocument("test" + str(i))
	# App.getDocument("test" + str(i)).saveAs(u"D:/Sudhir/MTP/FreeCAD/data" + "/test" + str(i) + ".FCStd")

	#Export to STL

for i in range(2):
	doc = App.getDocument("test" + str(i))
	# FreeCAD.open(u"D:/Sudhir/MTP/FreeCAD/data/test" + str(i) + ".FCStd")
	App.setActiveDocument("test" + str(i))
	App.ActiveDocument=App.getDocument("test" + str(i))
	Gui.ActiveDocument=Gui.getDocument("test" + str(i))
	__objs__=[]
	__objs__.append(FreeCAD.getDocument("test" + str(i)).getObject("Cut"))
	import Mesh
	Mesh.export(__objs__,u"D:/Sudhir/MTP/FreeCAD/data/test" + str(i) + ".stl")
	del __objs__
	#FEM
	import ObjectsFem
	#analysis
	analysis_object = ObjectsFem.makeAnalysis(doc, "Analysis")
	# material
	material_object = ObjectsFem.makeMaterialSolid(doc, "SolidMaterial")
	mat = material_object.Material
	mat['Name'] = "Steel-Generic"
	mat['YoungsModulus'] = "210000 MPa"
	mat['PoissonRatio'] = "0.30"
	mat['Density'] = "7900 kg/m^3"
	material_object.Material = mat
	analysis_object.addObject(material_object)
	# fixed_constraint
	fixed_constraint = ObjectsFem.makeConstraintFixed(doc, "FemConstraintFixed")
	fixed_constraint.References = [(doc.Box, "Face1")]
	analysis_object.addObject(fixed_constraint)
	# force_constraint
	force_constraint = ObjectsFem.makeConstraintForce(doc, "FemConstraintForce")
	force_constraint.References = [(doc.Box, "Face2")]
	force_constraint.Force = 1000.0
	force_constraint.Direction = (doc.Box, ["Edge5"])
	force_constraint.Reversed = True
	analysis_object.addObject(force_constraint)
	# solver (we gone use the well tested CcxTools solver object)
	solver_object = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX")
	solver_object.GeometricalNonlinearity = 'linear'
	solver_object.ThermoMechSteadyState = True
	solver_object.MatrixSolverType = 'default'
	solver_object.IterationsControlParameterTimeUse = False
	analysis_object.addObject(solver_object)
	#Mesh
	import FemGui
	FemGui.setActiveAnalysis(App.activeDocument().Analysis)
	ObjectsFem.makeMeshNetgen(FreeCAD.ActiveDocument, 'FEMMeshNetgen')
	FreeCAD.ActiveDocument.ActiveObject.Shape = FreeCAD.ActiveDocument.Cut
	FemGui.getActiveAnalysis().addObject(FreeCAD.ActiveDocument.ActiveObject)
	FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)
	Gui.activeDocument().resetEdit()
	#Solve
	import FemGui
	FemGui.setActiveAnalysis(doc.Analysis)
	#run the analysis all in one
	from femtools import ccxtools
	fea = ccxtools.FemToolsCcx()
	fea.purge_results()
	fea.run()
	#Save The Results
	femmesh_obj = App.ActiveDocument.getObject("Result_mesh").FemMesh
	result = App.ActiveDocument.getObject("CalculiX_static_results")
	import femmesh.femmesh2mesh
	out_mesh = femmesh.femmesh2mesh.femmesh_2_mesh(femmesh_obj, result)
	import Mesh
	Mesh.show(Mesh.Mesh(out_mesh))
	result
	displacement = result.DisplacementLengths
	import numpy
	# App.getDocument("test" + str(i)).saveAs(u"D:/Sudhir/MTP/FreeCAD/simulate_model" + "/test" + str(i) + ".FCStd")
	numpy.savetxt("D:/Sudhir/MTP/FreeCAD/data/output" + "/disp" + str(i) + ".csv", displacement,delimiter=",")
	stress = result.StressValues
	numpy.savetxt("D:/Sudhir/MTP/FreeCAD/data/output" + "/stress" + str(i) + ".csv",stress,delimiter=",")
	Gui.SendMsgToActiveView("Save")
	App.getDocument("test" + str(i)).save()