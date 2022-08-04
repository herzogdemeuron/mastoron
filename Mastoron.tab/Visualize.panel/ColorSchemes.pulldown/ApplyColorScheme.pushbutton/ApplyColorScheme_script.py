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

keys = set()
for item in selection:
    key = _(item).get(schemeName)
    if str(selectedOption.type) == 'Invalid':
        key = _(revitron.DOC.GetElement(key)).get('Name')
    keys.add(key)

scheme = ColorScheme().load(schemeName)
if not scheme:
    scheme = ColorScheme().generate(schemeName, keys)
    if not scheme:
        sys.exit()
elif scheme:
    ColorScheme().update(scheme, keys)

ColorScheme().save(scheme)

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]

with revitron.Transaction():
    for element in selection:
        key = _(element).get(schemeName)
        if str(selectedOption.type) == 'Invalid':
            key = _(revitron.DOC.GetElement(key)).get('Name')
        colorHEX = scheme['data'][key]
        colorRGB = mastoron.Color.HEXtoRGB(colorHEX)
        mastoron.ElementOverrides(element).set(colorRGB, patternId)