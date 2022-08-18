import sys
import mastoron
import os.path as op
from pyrevit import forms

SAVE = 'Save'
XAML_FILES_DIR = op.dirname(__file__)


class ColorSchemeEditor(mastoron.ColorSwitchWindow):
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

    def __init__(self, context, title, width, height, **kwargs):
        '''
        Initialize user input window.
        '''
        super(ColorSchemeEditor, self).__init__(
            context, XAML_FILES_DIR, title, width, height, **kwargs, 
            )

    def save(self, sender, args):
        self.Close()
        self.response = SAVE


scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

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
