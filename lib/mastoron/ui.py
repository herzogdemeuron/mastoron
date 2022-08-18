import clr
import os.path as op
from mastoron.variables import SAVE
from pyrevit import forms
from pyrevit import framework
from pyrevit.forms import WPFWindow
clr.AddReference('System.Windows.forms')
from System.Windows.Media import BrushConverter


class ColorSwitchWindow(forms.CommandSwitchWindow):
    '''
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    '''

    def __init__(self,
                context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs):
        '''
        Initialize user input window.
        '''
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
        for button in self.button_list.Children:
            key = button.Content
            if key:
                brush = BrushConverter().ConvertFrom(self.scheme['data'][key])
                button.Background = brush

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
    '''
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    '''

    xaml_source = 'ColorSwitchWindow.xaml'

    def __init__(self,
                context,
                xamlFilesDir,
                xamlSource,
                title,
                width,
                height,
                **kwargs):
        '''
        Initialize user input window.
        '''
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
