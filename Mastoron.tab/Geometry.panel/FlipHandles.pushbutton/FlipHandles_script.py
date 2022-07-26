import sys
import random
import revitron


selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

FACING = 'flipFacing'
HAND = 'flipHand'
CHOICES = [FACING, HAND]

with revitron.Transaction():
    for element in selection:
        location = element.Location.Point
        choice = random.choice(CHOICES)
        if choice == FACING:
            element.flipFacing()
        if choice == HAND:
            element.flipHand()
            