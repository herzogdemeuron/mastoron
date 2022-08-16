import sys
import clr
import mastoron
from pyrevit import forms
clr.AddReference('System.Windows.forms')
from System.Windows.Media import BrushConverter


SAVE = '~SAVE~'


class ColorSchemeEditor(forms.CommandSwitchWindow):
    '''Extended form to select from a list of command options.

    Args:
        context (list[str]): list of command options to choose from
        switches (list[str]): list of on/off switches
        message (str): window title message
        config (dict): dictionary of config dicts for options or switches
        recognize_access_key (bool): recognize '_' as mark of access key
    
    '''

    def colorButtons(self, scheme):
        for button in self.button_list.Children:
            key = button.Content
            button.Background = BrushConverter().ConvertFrom(scheme['data'][key])

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
        dlg.colorButtons(scheme)
        dlg.ShowDialog()
        return dlg.response

print(forms.XAML_FILES_DIR)

names = []
for scheme in mastoron.ColorScheme().schemes:
    names.append(scheme['name'])

selection = forms.CommandSwitchWindow.show(sorted(names),
        message='Choose Color Scheme:')

if not selection:
    sys.exit()

scheme = mastoron.ColorScheme().load(selection)

scheme['data'][SAVE] = '#ffffffff'

while True:
    key= ColorSchemeEditor.show(scheme, message='Search Key:')

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
