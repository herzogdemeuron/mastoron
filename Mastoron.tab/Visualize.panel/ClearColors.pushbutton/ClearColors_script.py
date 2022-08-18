import sys
import revitron
import mastoron
from mastoron.variables import MASTORON_COLORSCHEME
from revitron import _


scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

mastoronElements = revitron.Filter(revitron.ACTIVE_VIEW.Id).byStringEquals(
    MASTORON_COLORSCHEME, scheme['name']).getElements()

if len(mastoronElements) < 1:
    sys.exit()

with revitron.Transaction():
    for element in mastoronElements:
        mastoron.ElementOverrides(element).clear()
        _(element).set(MASTORON_COLORSCHEME, '')
