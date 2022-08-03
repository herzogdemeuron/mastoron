import sys
import mastoron
from pyrevit import forms


path = forms.pick_file(file_ext='json',
        title='Load Color Scheme:')

if not path:
    sys.exit()

scheme = mastoron.ColorScheme().fromJSON(path)
mastoron.ColorScheme().save(scheme)