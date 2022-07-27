import revitron
from revitron import _
import mastoron


selection = revitron.Selection().get()
floorType = revitron.Filter().byCategory('Floors').onlyTypes().getElementIds()[0]

with revitron.Transaction():
    mastoron.BooleanFloors(floors=selection, floorType=floorType)
