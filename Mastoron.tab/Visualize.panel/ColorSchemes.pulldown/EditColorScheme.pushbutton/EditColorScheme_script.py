import sys
import mastoron
import os.path as op
from pyrevit import forms
from mastoron.variables import SAVE


scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

xamlFilesDir = op.dirname(__file__)
xamlSource = 'ColorSwitchWindow.xaml'

while True:
    key = mastoron.ColorSchemeEditor.show(
        scheme, xamlFilesDir, xamlSource, message='Search Key:')
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
