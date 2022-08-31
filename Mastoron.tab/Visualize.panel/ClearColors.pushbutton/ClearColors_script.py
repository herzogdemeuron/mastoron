import sys
import json
import revitron
import mastoron
from mastoron.variables import MASTORON_COLORSCHEME, NAME
from revitron import _


activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

overriddenElements = mastoron.AffectedElements.get(activeView)

if len(overriddenElements) < 1:
    sys.exit()

with revitron.Transaction():
    for id, value in overriddenElements.items():
        if value == scheme[NAME]:
            elementId = revitron.DB.ElementId(int(id))
            element = revitron.DOC.GetElement(elementId)
            mastoron.ElementOverrides(activeView, element).clear()
            del overriddenElements[id]
    
    _(activeView).set(MASTORON_COLORSCHEME, json.dumps(overriddenElements)) 
