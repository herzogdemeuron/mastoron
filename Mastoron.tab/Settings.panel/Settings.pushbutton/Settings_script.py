import revitron
import mastoron
import json
from pyrevit import forms

config = {}
try:
    config = mastoron.ConfigStorage().config
except:
    pass

path = forms.save_file(file_ext='json', default_name='mastoronConfig')

if path:
    with open(path, 'w') as f:
        config = json.dumps(config)
        f.write(config)
        
    with revitron.Transaction():
        mastoron.ConfigStorage.setPath(path)