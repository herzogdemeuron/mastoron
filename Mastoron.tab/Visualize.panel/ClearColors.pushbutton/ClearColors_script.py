import sys
import revitron
import mastoron
from mastoron.variables import NAME
from revitron import _


activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser(excludeViews=activeView.Id)
if not scheme:
    sys.exit()
    
if not str(activeView.Id) in mastoron.AffectedViews().affectedViews[scheme[NAME]]:
    sys.exit()

overriddenElements = mastoron.AffectedElements().get(scheme, viewId=activeView.Id)

if len(overriddenElements) < 1:
    sys.exit()

with revitron.Transaction():
    for elementId in overriddenElements:
        element = mastoron.Convert.toRevitElement(elementId)
        mastoron.ElementOverrides(activeView, element).clear()
    
    mastoron.AffectedViews().delete(scheme, activeView.Id)