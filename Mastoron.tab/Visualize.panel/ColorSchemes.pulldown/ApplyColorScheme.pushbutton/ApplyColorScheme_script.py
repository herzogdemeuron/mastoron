import sys
import revitron
import mastoron
from revitron import _
from pyrevit import forms


selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

options = mastoron.ProcessOptions(selection, staticParams=['Area'])
if options:
    selectedSwitch = forms.CommandSwitchWindow.show(sorted(options),
        message='Visualize parameter:')

if not selectedSwitch:
    sys.exit()

selectedOption = options[selectedSwitch]
schemeName = selectedOption.name

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    mastoron.ColorScheme.apply(selection,
                    schemeName,
                    selectedOption.isInstance,
                    selectedOption.type,
                    patternId)
