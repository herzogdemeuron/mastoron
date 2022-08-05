import sys
import mastoron
import revitron
from revitron import _
from pyrevit import forms

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

subCatSets = []
for element in selection:
    subCatSet = set()
    lines = _(element).getGeometry().getCurves()
    for line in lines:
        subcategory = revitron.DOC.GetElement(line.GraphicsStyleId).Name
        if subcategory:
            subCatSet.add(subcategory)
    subCatSets.append(subCatSet)

if subCatSets:
    allSharedSubCats = subCatSets[0]
    for subCatSet in subCatSets[1:]:
        allSharedSubCats = allSharedSubCats.intersection(subCatSet)

if allSharedSubCats:
    selectedSubcat = forms.CommandSwitchWindow.show(sorted(allSharedSubCats),
        message='Create Floor from subcategory:')

floorType = revitron.Filter().byCategory('Floors').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

floors = []
with revitron.Transaction():
    for element in selection:
        floor = mastoron.FloorCreator(levels, element, floorType).fromFamilyModelLines(selectedSubcat)
        if floor:
            floors.append(floor.Id)
        
revitron.Selection.set(floors)

