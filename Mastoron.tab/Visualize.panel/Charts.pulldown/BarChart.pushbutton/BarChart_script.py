import sys
import mastoron
import revitron
import os.path as op
from mastoron.variables import ROUNDING_DECIMALS
from revitron import _
from pyrevit import forms


COUNT = 'Count'
NUMBER_PARAMS = ['Integer', 'Double']
DELIM = '-'


scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

selection = revitron.Selection().get()

if len(selection) < 1:
    sys.exit()

params = mastoron.ProcessOptions(selection, staticParams=['Mass Area'])
if params:
    dataParamName = forms.CommandSwitchWindow.show(sorted(params),
        message='Choose value:')
if not dataParamName:
    sys.exit()

instanceParam = True
try:
    param = revitron.Parameter(selection[0], dataParamName).parameter
    paramStorageType = str(param.StorageType)
except:
    instanceParam = False
    elType = revitron.DOC.GetElement(selection[0].GetTypeId())
    param = revitron.Parameter(elType, dataParamName).parameter
    paramStorageType = str(param.StorageType)

if not paramStorageType in NUMBER_PARAMS:
    dataParamName = COUNT

paramTotals = {}
for element in selection:
    if scheme['isInstance']:
        key = _(element).get(scheme['name'])
        try:
            key = str(round(key, ROUNDING_DECIMALS))
        except:
            key = str(key)
    else:
        elType = revitron.DOC.GetElement(element.GetTypeId())
        key = _(elType).get(scheme['name'])
        try:
            key = str(round(key, ROUNDING_DECIMALS))
        except:
            key = str(key)

    if not dataParamName == COUNT:
        value = _(element).get(dataParamName)
    else:
        value = 1
    
    if not value:
        value = 0
    if not key in paramTotals:
        paramTotals[key] = float(value)
    else:
        paramTotals[key] += float(value)

revitron.Selection().set([])
xamlFilesDir = op.dirname(__file__)
xamlSource = 'BarChartWindow.xaml'
selectedParam = mastoron.BarGraphWindow.show(scheme,
                                            xamlFilesDir,
                                            xamlSource,
                                            paramTotals,
                                            dataParamName,
                                            message='Search Key:')

if selectedParam:
    elements = revitron.Filter(selection).byStringEquals(scheme['name'], selectedParam).getElementIds()
    revitron.Selection().set(elements)