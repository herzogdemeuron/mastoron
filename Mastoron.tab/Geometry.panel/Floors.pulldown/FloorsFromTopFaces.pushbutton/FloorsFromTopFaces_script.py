import sys
import mastoron
import revitron
from pyrevit import forms
from revitron import _

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

floorType = revitron.Filter().byCategory('Floors').onlyTypes().getElementIds()[0]
levels = revitron.Filter().byCategory('Levels').noTypes().getElements()
doc = revitron.DOC

userInput = forms.ask_for_string(
    default='0.0',
    prompt='Enter offset distance:',
    title='Floors from top faces')

try:
    offset = float(userInput)
except:
    print('Invalid input. Using 0.0 Offset')
    offset = 0.0

deleteInput = forms.alert(
    msg='Delete input geometry?',
    yes=True,
    no=True)

if deleteInput:
    allParams = set()
    for element in selection:
        for param in element.ParametersMap:
            allParams.add(param.Definition.Name)

    transferParams = forms.SelectFromList.show(sorted(allParams),
        button_name='Select Item',
        title='Select Parameters to transfer:',
        multiselect=True)

floors = []
with revitron.Transaction():
    for element in selection:
        elementFloors = mastoron.FloorCreator(levels, element, floorType).fromTopFaces(offset)
        if deleteInput:
            transferData = {}
            for param in transferParams:
                transfervalue = None
                try:
                    transfervalue = _(element).get(param)
                except:
                    pass
                transferData[param] = transfervalue

        for floor in elementFloors:
            floors.append(floor.Id)
            if deleteInput:
                for param, value in transferData.items():
                    if value:
                        _(floor).set(param, value)

        if deleteInput:
            _(element).delete()

revitron.Selection.set(floors)

