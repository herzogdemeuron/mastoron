import sys
import revitron
import mastoron
from mastoron.variables import GRADIENTS
from mastoron.variables import NAME, IS_INSTANCE, PARAM_TYPE
from revitron import _

activeView = revitron.ACTIVE_VIEW

scheme = mastoron.ColorScheme.getFromUser(exclude=GRADIENTS)
if not scheme:
    sys.exit()

overriddenElements = mastoron.AffectedElements.get(activeView)
if len(overriddenElements) < 1:
    sys.exit()

viewElements = mastoron.AffectedElements.filter(overriddenElements, scheme)
if len(viewElements) < 1:
    sys.exit()

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    mastoron.ColorScheme.apply(activeView,
                    viewElements,
                    scheme[NAME],
                    scheme[IS_INSTANCE],
                    scheme[PARAM_TYPE],
                    patternId)