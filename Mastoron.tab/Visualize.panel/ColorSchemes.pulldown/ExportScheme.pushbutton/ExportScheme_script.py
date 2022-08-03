import sys
import os
import mastoron
from pyrevit import forms
from pyrevit import script

schemes = mastoron.ColorScheme().schemes
names = []
for scheme in schemes:
    names.append(scheme['name'])

selection = forms.CommandSwitchWindow.show(sorted(names),
        message='Visualize parameter:')

if not selection:
    sys.exit()

scheme = mastoron.ColorScheme().load(selection)
file = mastoron.ColorScheme.toJSON(scheme)

script.show_folder_in_explorer(os.path.dirname(file))