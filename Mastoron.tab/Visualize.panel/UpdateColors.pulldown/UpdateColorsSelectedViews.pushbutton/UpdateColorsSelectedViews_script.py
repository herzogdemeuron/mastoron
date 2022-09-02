import sys
import revitron
import mastoron
from mastoron.variables import GRADIENTS
from mastoron.variables import NAME, IS_INSTANCE, PARAM_TYPE, SCHEME_NAME, VIEWS
from revitron import _
from pyrevit import forms


activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser(exclude=GRADIENTS)
if not scheme:
    sys.exit()

views = []
viewsDict = {}
for viewId in mastoron.AffectedViews().affectedViews[scheme[NAME]]:
        elementId = revitron.DB.ElementId(int(viewId))
        view = revitron.DOC.GetElement(elementId)
        views.append(view.Name)
        viewsDict[view.Name] = view

viewsSelected = forms.SelectFromList.show(sorted(views),
        title='Choose views:', multiselect=True)

if not viewsSelected:
    sys.exit()

if not type(viewsSelected) == list:
    viewsSelected = [viewsSelected]

viewsElements = {}

for viewName in viewsSelected:
    overriddenElements = mastoron.AffectedElements.get(activeView)
    if len(overriddenElements) < 1:
        continue
    viewElements = mastoron.AffectedElements.filter(overriddenElements, scheme)
    viewsElements[viewName] = viewElements

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    for viewName, elements in viewsElements.items():
        mastoron.ColorScheme.apply(viewsDict[viewName],
                        elements,
                        scheme[NAME],
                        scheme[IS_INSTANCE],
                        scheme[PARAM_TYPE],
                        patternId)