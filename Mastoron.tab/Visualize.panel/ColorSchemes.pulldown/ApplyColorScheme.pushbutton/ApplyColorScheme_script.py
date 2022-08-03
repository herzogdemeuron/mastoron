import sys
import revitron
import mastoron
from mastoron import ColorScheme
from revitron import _
from pyrevit import forms


selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

options = mastoron.ProcessOptions(selection)
if options:
    selectedSwitch = forms.CommandSwitchWindow.show(sorted(options),
        message='Visualize parameter:')

if not selectedSwitch:
    sys.exit()

selectedOption = options[selectedSwitch]
schemeName = selectedOption.name

values = set()
for item in selection:
    value = _(item).get(schemeName)
    if str(selectedOption.type) == 'Invalid':
        value = _(revitron.DOC.GetElement(value)).get('Name')
    values.add(value)

scheme = ColorScheme().load(schemeName)
if not scheme:
    scheme = ColorScheme.generate(schemeName, values)
elif scheme:
    ColorScheme.update(scheme, values)

ColorScheme().save(scheme)

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    for element in selection:
        value = _(element).get(schemeName)
        if str(selectedOption.type) == 'Invalid':
            value = _(revitron.DOC.GetElement(value)).get('Name')
        colorHEX = scheme['data'][value]
        colorRGB = mastoron.Color.HEXtoRGB(colorHEX)
        mastoron.ElementOverrides(element).set(colorRGB, patternId)