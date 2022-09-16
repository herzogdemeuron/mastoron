import sys
import revitron
import mastoron
from mastoron.variables import GRADIENTS
from mastoron.variables import NAME, IS_INSTANCE, PARAM_TYPE
from revitron import _


activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser(excludeSchemes=GRADIENTS, excludeViews=activeView.Id)
if not scheme:
    sys.exit()

overriddenElements = mastoron.AffectedElements().get(scheme, viewId=activeView.Id)
if len(overriddenElements) < 1:
    sys.exit()

overriddenElements = [mastoron.Convert.toRevitElement(x) for x in overriddenElements]

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    mastoron.ColorScheme.apply(activeView,
                    overriddenElements,
                    scheme[NAME],
                    scheme[IS_INSTANCE],
                    scheme[PARAM_TYPE],
                    patternId)