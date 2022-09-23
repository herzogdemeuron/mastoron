import sys
import mastoron
import revitron

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

floorType = revitron.Filter().byCategory('Floors').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

floors = []
with revitron.Transaction():
    for element in selection:
        elementFloors = mastoron.FloorCreator(levels, element, floorType).fromBottomFaces()
        for floor in elementFloors:
            floors.append(floor.Id)

revitron.Selection.set(floors)

