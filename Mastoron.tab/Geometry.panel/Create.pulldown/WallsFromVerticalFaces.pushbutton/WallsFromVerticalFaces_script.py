import sys
import mastoron
import revitron
from pyrevit import forms
from revitron import _

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

wallTypes = revitron.Filter().byCategory('Walls').onlyTypes().getElements()
wallsDict = {}

for wallType in wallTypes:
    wallsDict[_(wallType).get('SYMBOL_NAME_PARAM')] = wallType.Id
res = forms.CommandSwitchWindow.show(wallsDict.keys(), title='Select Wall Type')
if not res:
    sys.exit()

wallType = wallsDict[res]

levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

walls = []
with revitron.Transaction():
    for element in selection:
        elementWalls = mastoron.WallCreator(levels, element, wallType).fromVerticalFaces()
        for wall in elementWalls:
            walls.append(wall.Id)

revitron.Selection.set(walls)

