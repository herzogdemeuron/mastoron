import sys
import json
import revitron
import mastoron
from mastoron import ColorScheme
from mastoron.variables import MASTORON_COLORSCHEME
from mastoron.variables import ROUNDING_DECIMALS
from mastoron.variables import GRADIENTS
from mastoron.variables import NAME, DATA
from revitron import _
from pyrevit import forms


def getKey(element, parameter, selectedOption):
    if selectedOption.isInstance:
        key = _(element).get(parameter)
    elif not selectedOption.isInstance:
        key = _(revitron.DOC.GetElement(element.GetTypeId())).get(parameter)
    if not key:
        return None
    if str(selectedOption.type) == 'Invalid':
        print('Cannot apply gradient, choose number or text parameter.')
        sys.exit()
    try:
        key = str(round(key, ROUNDING_DECIMALS))
    except:
        key = str(key)
    return key

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

options = mastoron.ProcessOptions(selection, staticParams=['Mass Area'])
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
    if key:
        keys.add(key)

start, end = int((54.0 / 360) * 100), int((174.0 / 360) * 100)
scheme = ColorScheme().generate(
    schemeName, keys, gradient=(start, end))
if not scheme:
    sys.exit()

scheme[NAME] = GRADIENTS
ColorScheme().save(scheme)

filter = revitron.Filter()
patternId = filter.byClass('FillPatternElement').noTypes().getElementIds()[0]
activeView = revitron.ACTIVE_VIEW
overriddenElements = mastoron.AffectedElements.get(activeView)

with revitron.Transaction():
    for element in selection:
        mastoron.ElementOverrides(activeView, element).clear()
        key = getKey(element, schemeName, selectedOption)
        if key:
            colorHEX = scheme[DATA][key]
            colorRGB = mastoron.Color.HEXtoRGB(colorHEX)
            mastoron.ElementOverrides(activeView, element).set(colorRGB, patternId)
            overriddenElements[str(element.Id)] = scheme[NAME]
    
    mastoron.AffectedElements.set(activeView, overriddenElements)
    mastoron.AffectedViews().save(scheme, activeView.Id)