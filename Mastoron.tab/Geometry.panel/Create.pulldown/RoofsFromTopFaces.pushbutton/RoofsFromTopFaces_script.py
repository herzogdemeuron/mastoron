import sys
import mastoron
import revitron

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

roofType = revitron.Filter().byCategory('Roofs').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

roofs = []
with revitron.Transaction():
    for element in selection:
        elementRoofs = mastoron.RoofCreator(levels, element, roofType).fromTopFaces()
        for roof in elementRoofs:
            roofs.append(roof.Id)

revitron.Selection.set(roofs)

