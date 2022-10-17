import sys
import mastoron
import revitron

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

railingType = revitron.Filter().byCategory('Railings').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

railings = []
with revitron.Transaction():
    for element in selection:
        elementRailings = mastoron.RailingCreator(levels, element, railingType).fromTopFaces()
        for railing in elementRailings:
            railings.append(railing.Id)

revitron.Selection.set(railings)

