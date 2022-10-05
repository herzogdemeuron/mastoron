import sys
import mastoron
import revitron

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

wallType = revitron.Filter().byCategory('Walls').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

walls = []
with revitron.Transaction():
    for element in selection:
        elementWalls = mastoron.WallCreator(levels, element, wallType).fromVerticalFaces()
        for wall in elementWalls:
            walls.append(wall.Id)

revitron.Selection.set(walls)

