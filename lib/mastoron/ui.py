import clr
import os.path as op
from mastoron.variables import DATA, SAVE, ROUNDING_DECIMALS
from pyrevit import forms
from pyrevit import framework
from pyrevit.forms import WPFWindow
clr.AddReference('System')
from System.Windows.Media import BrushConverter
from System.Windows.Media import Brushes


class ColorSwitchWindow(forms.CommandSwitchWindow):
    """
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    """

    def __init__(self,
                context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs):
        """
        Initialize user input window.
        """
        WPFWindow.__init__(self,
                           op.join(xamlFilesDir, xamlSource),
                           handle_esc=True)
        self.Title = title or 'pyRevit'
        self.Width = width
        self.Height = height

        self._context = context
        self.response = None

        # parent window?
        owner = kwargs.get('owner', None)
        if owner:
            # set wpf windows directly
            self.Owner = owner
            self.WindowStartupLocation = \
                framework.Windows.WindowStartupLocation.CenterOwner

        self._setup(**kwargs)

    def colorButtons(self):
        """
        Sets the background color for all buttons according to the corresponding
        hex value in color scheme. 
        """
        for button in self.button_list.Children:
            key = button.Content
            if key:
                try:
                    brush = BrushConverter().ConvertFrom(self.scheme[DATA][key])
                    button.Background = brush
                except:
                    pass

    @classmethod
    def show(cls, 
            scheme,  #pylint: disable=W0221
            xamlFilesDir,
            xamlSource,
            title='User Input',
            width=forms.DEFAULT_INPUTWINDOW_WIDTH,
            height=forms.DEFAULT_INPUTWINDOW_HEIGHT,
            **kwargs):
        """
        Show user input window.

        Args:
            context (any): window context element(s)
            title (str): window title
            width (int): window width
            height (int): window height
            **kwargs (any): other arguments to be passed to window
        """
        context = sorted(scheme['data'].keys())
        dlg = cls(context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs)
        dlg.scheme = scheme
        dlg.colorButtons()
        dlg.ShowDialog()
        return dlg.response

        
class ColorSchemeEditor(ColorSwitchWindow):
    """
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    """

    def __init__(self,
                context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs):
        """
        Initialize user input window.
        """
        super(ColorSchemeEditor, self).__init__(context,
                                                xamlFilesDir,
                                                xamlSource,
                                                title,
                                                width,
                                                height,
                                                **kwargs)

    def save(self, sender, args):
        self.Close()
        self.response = SAVE


class BarGraphWindow(ColorSwitchWindow):
    """
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    """

    def __init__(self,
                context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs):
        """
        Initialize user input window.
        """
        super(BarGraphWindow, self).__init__(context,
                                            xamlFilesDir,
                                            xamlSource,
                                            title,
                                            width,
                                            height,
                                            **kwargs)

    def resizeButtons(self, paramTotals):
        """
        Set the width of all buttons according to the total of the parameter values
        it represents.

        Args:
            paramTotals (dict): {"<colorSchemeParamValue>":"<dataParamValueTotal>"}
        """
        maxValue = max(paramTotals.values())
        scaleFactor =  (forms.DEFAULT_CMDSWITCHWND_WIDTH - 170) / maxValue
        for button in self.button_list.Children:
            key = button.Content
            rawValue = int(paramTotals[key])
            value = rawValue * scaleFactor
            button.Width = value

    @classmethod
    def show(cls, 
            scheme,  #pylint: disable=W0221
            xamlFilesDir,
            xamlSource,
            paramTotals, 
            dataParamName,
            title='User Input',
            width=forms.DEFAULT_INPUTWINDOW_WIDTH,
            height=forms.DEFAULT_INPUTWINDOW_HEIGHT, **kwargs):
        """
        Show user input window.

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
        context = collections.OrderedDict(sortedTuples).keys()
        title = dataParamName + ' by ' + scheme['name']

        dlg = cls(context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs)
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