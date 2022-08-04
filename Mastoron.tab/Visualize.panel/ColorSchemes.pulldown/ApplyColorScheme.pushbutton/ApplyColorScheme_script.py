import sys
import revitron
import mastoron
from mastoron import ColorScheme
from revitron import _
from pyrevit import forms


def getKey(element, parameter, selectedOption):
    if selectedOption.isInstance:
        key = _(element).get(parameter)
    elif not selectedOption.isInstance:
        key = _(revitron.DOC.GetElement(element.GetTypeId())).get(parameter)
    if str(selectedOption.type) == 'Invalid':
        key = _(revitron.DOC.GetElement(key)).get('Name')
    try:
        key = str(round(key, 3))
    except:
        key = str(key)
    return key

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
for element in selection:
    key = getKey(element, schemeName, selectedOption)
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
        key = getKey(element, schemeName, selectedOption)
        colorHEX = scheme['data'][key]
        colorRGB = mastoron.Color.HEXtoRGB(colorHEX)
        mastoron.ElementOverrides(element).set(colorRGB, patternId)