import sys
import random
import revitron
from rpw.ui.forms import TextInput


selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

ids = []
for element in selection:
    ids.append(element.Id)

percent = TextInput('Percentage:', default="42",
                description="Current selection will be reduced to percentage.")
itemCount = int(len(ids) * (float(percent) / 100))
reduced_ids = [ids[i] for i in random.sample(range(0, len(ids)), itemCount)]
revitron.Selection.set(reduced_ids)