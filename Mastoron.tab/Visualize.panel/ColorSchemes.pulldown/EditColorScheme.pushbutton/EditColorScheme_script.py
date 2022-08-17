import sys
import clr
import mastoron
import os.path as op
from pyrevit import forms
from pyrevit import framework
from pyrevit.forms import WPFWindow
clr.AddReference('System.Windows.forms')
from System.Windows.Media import BrushConverter

SAVE = 'Save'
XAML_FILES_DIR = op.dirname(__file__)


class ColorSchemeEditor(forms.CommandSwitchWindow):
    '''
    Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    '''

    def __init__(self, context, title, width, height, **kwargs):
        '''
        Initialize user input window.
        '''
        WPFWindow.__init__(self,
                           op.join(XAML_FILES_DIR, self.xaml_source),
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

    def save(self, sender, args):
        self.Close()
        self.response = SAVE

    def colorButtons(self):
        for button in self.button_list.Children:
            key = button.Content
            brush = BrushConverter().ConvertFrom(self.scheme['data'][key])
            button.Background = brush

    @classmethod
    def show(cls, scheme,  #pylint: disable=W0221
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
        context = sorted(scheme['data'].keys())
        dlg = cls(context, title, width, height, **kwargs)
        dlg.scheme = scheme
        dlg.colorButtons()
        dlg.ShowDialog()
        return dlg.response


names = []
for scheme in mastoron.ColorScheme().schemes:
    names.append(scheme['name'])

selection = forms.CommandSwitchWindow.show(sorted(names),
        message='Choose Color Scheme:')

if not selection:
    sys.exit()

scheme = mastoron.ColorScheme().load(selection)

while True:
    key = ColorSchemeEditor.show(scheme, message='Search Key:')
    if not key:
        sys.exit()
    if key == SAVE:
        break

    defaultColor = scheme['data'][key]
    if not defaultColor.startswith('#'):
        defaultColor = '#' + defaultColor
    if not len(defaultColor) == 9:
        defaultColor = defaultColor[:1] + 'ff' + defaultColor[1:]
    color = forms.ask_for_color(default=defaultColor)
    if not color:
        continue
    color = color[:1] + color[3:]
    scheme['data'][key] = color

mastoron.ColorScheme().save(scheme)
