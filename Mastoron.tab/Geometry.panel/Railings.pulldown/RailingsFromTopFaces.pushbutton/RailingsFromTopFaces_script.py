import sys
import mastoron
import revitron
from pyrevit import forms

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

selected_option, switches = \
    forms.CommandSwitchWindow.show(['Create Railings'],
        switches={'Include Openings': False},
        message='Select Option:',
        recognize_access_key=True
        )

includeInnerLoops = switches['Include Openings']

railingType = revitron.Filter().byCategory('Railings').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC


railings = []
with revitron.Transaction():
    for element in selection:
        elementRailings = mastoron.RailingCreator(levels, element, railingType).fromTopFaces(includeInnerLoops)
        for railing in elementRailings:
            railings.append(railing.Id)

revitron.Selection.set(railings)

