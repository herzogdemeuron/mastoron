import clr
import sys
import mastoron
import revitron
import os.path as op
from mastoron.variables import ROUNDING_DECIMALS
from revitron import _
from pyrevit import forms
from pyrevit import framework
clr.AddReference('System')
from System.Windows.Media import Brushes

XAML_FILES_DIR = op.dirname(__file__)
COUNT = 'Count'
NUMBER_PARAMS = ['Integer', 'Double']
DELIM = '-'


class BarGraphWindow(mastoron.ColorSwitchWindow):
    '''
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    '''

    xaml_source = 'BarChartWindow.xaml'

    def __init__(self, context, title, width, height, **kwargs):
        '''
        Initialize user input window.
        '''
        super(BarGraphWindow, self).__init__(
            context, XAML_FILES_DIR, title, width, height, **kwargs, 
            )

    def resizeButtons(self, paramTotals):
        maxValue = max(paramTotals.values())
        scaleFactor =  (forms.DEFAULT_CMDSWITCHWND_WIDTH - 170) / maxValue
        for button in self.button_list.Children:
            key = button.Content
            rawValue = int(paramTotals[key])
            value = rawValue * scaleFactor
            button.Width = value

    @classmethod
    def show(cls, scheme,  #pylint: disable=W0221
            paramTotals, 
            dataParamName,
            title='User Input',
            width=forms.DEFAULT_INPUTWINDOW_WIDTH,
            height=forms.DEFAULT_INPUTWINDOW_HEIGHT, **kwargs):
        """Show user input window.

        Args:
            context (any): window context element(s)
            title (str): window title
            width (int): window width
            height (int): window height
            **kwargs (any): other arguments to be passed to window
        """
        import operator
        import collections
        for key in scheme['data'].keys():
            if not key in paramTotals.keys():
                del scheme['data'][key]
            if not key:
                del scheme['data'][key]
        sortedTuples = sorted(paramTotals.items(), key=operator.itemgetter(1))
        buttonContent = collections.OrderedDict(sortedTuples).keys()
        title = dataParamName + ' by ' + scheme['name']
        dlg = cls(buttonContent, title, width, height, **kwargs)
        dlg.scheme = scheme
        dlg.colorButtons()
        dlg.resizeButtons(paramTotals)
        dlg.title.Content = title
        for value in collections.OrderedDict(sortedTuples).values():
            label = framework.Controls.Label()
            label.Content = str(round(value, ROUNDING_DECIMALS))
            label.Foreground = Brushes.LightGray
            label.FontSize = 11.2
            dlg.valueList.Children.Add(label)
        dlg.ShowDialog()
        return dlg.response


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
selectedParam = BarGraphWindow.show(
    scheme, paramTotals, dataParamName, message='Search Key:')

if selectedParam:
    elements = revitron.Filter(selection).byStringEquals(scheme['name'], selectedParam).getElementIds()
    revitron.Selection().set(elements)