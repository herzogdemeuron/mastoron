import sys
import revitron
import mastoron
from mastoron.variables import GRADIENTS
from mastoron.variables import NAME, IS_INSTANCE, PARAM_TYPE
from revitron import _
from pyrevit import forms


activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser(excludeSchemes=GRADIENTS)
if not scheme:
    sys.exit()

if not scheme[NAME] in mastoron.AffectedViews().affectedViews:
    print('Color scheme "{}" is not applied in any view!'.format(scheme[NAME]))
    sys.exit()

with revitron.Transaction():
    views = []
    viewsDict = {}
    affectedViews = mastoron.AffectedViews().get(scheme)
    for viewId in affectedViews.keys():
        view = mastoron.Convert.toRevitElement(viewId)
        if not view:
            mastoron.AffectedViews().delete(scheme, viewId)
            continue
        views.append(view.Name)
        viewsDict[view.Name] = viewId

    viewsSelected = forms.SelectFromList.show(sorted(views),
            title='Choose views:', multiselect=True)

    if not viewsSelected:
        sys.exit()

    if not type(viewsSelected) == list:
        viewsSelected = [viewsSelected]

    filter = revitron.Filter()
    patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

    for viewId, elementIds in affectedViews.items():
        if viewId not in viewsDict.values():
            continue
        view = mastoron.Convert.toRevitElement(viewId)
        elements = [mastoron.Convert.toRevitElement(x) for x in elementIds]
        mastoron.ColorScheme.apply(view,
                        elements,
                        scheme[NAME],
                        scheme[IS_INSTANCE],
                        scheme[PARAM_TYPE],
                        patternId)