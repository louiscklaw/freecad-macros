#!/usr/bin/env python2

import FreeCAD
from PySide import QtGui

doc_dir = "/home/logic/_workspace/freecad_scripts/freecad_test"

def _is_a_part(element):
	return (element is not None) and hasattr(element,'sourceFile')

def _update_parts(parts, name):
	App = FreeCAD
	for part in parts:
		was_open = False
		if part.sourceFile in [ d.FileName for d in FreeCAD.listDocuments().values() ]:
			doc = [ d for d in FreeCAD.listDocuments().values() if d.FileName == part.sourceFile][0]
			App.setActiveDocument(doc.Label)
			was_open = True
		else:
			doc = App.openDocument(os.path.join([doc_dir, part.sourceFile]))
			App.setActiveDocument(doc.Label)
		App.ActiveDocument=App.getDocument(doc.Label)
		_update_parts(filter(_is_a_part, App.ActiveDocument.Objects), doc.Label)
		App.ActiveDocument.save()
		if not was_open:
			App.closeDocument(doc.Label)
	App.setActiveDocument(name)
	App.ActiveDocument=App.getDocument(name)
	for obj in App.ActiveDocument.Objects:
 		obj.touch()
	App.ActiveDocument.recompute()

App.ActiveDocument.save()
_update_parts(filter(_is_a_part, FreeCAD.ActiveDocument.Objects),  FreeCAD.ActiveDocument.Label)
