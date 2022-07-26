import sys
import mastoron
import revitron
from revitron import _

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
with revitron.Transaction():
    for element in revitron.Selection().get():
        levelName = mastoron.Level.getLevelName(element, levels)
        _(element).set('Mass Level', levelName, 'Text')
