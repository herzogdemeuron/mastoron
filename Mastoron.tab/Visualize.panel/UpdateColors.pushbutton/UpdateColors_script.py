import sys
import revitron
import mastoron
from mastoron.variables import GRADIENTS
from mastoron.variables import MASTORON_COLORSCHEME
from mastoron.variables import NAME, IS_INSTANCE, PARAM_TYPE
from revitron import _


scheme = mastoron.ColorScheme.getFromUser(exclude=GRADIENTS)
if not scheme:
    sys.exit()

mastoronElements = revitron.Filter(revitron.ACTIVE_VIEW.Id).byStringEquals(
    MASTORON_COLORSCHEME, scheme[NAME]).getElements()

if len(mastoronElements) < 1:
    sys.exit()

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    mastoron.ColorScheme.apply(mastoronElements,
                    scheme[NAME],
                    scheme[IS_INSTANCE],
                    scheme[PARAM_TYPE],
                    patternId)