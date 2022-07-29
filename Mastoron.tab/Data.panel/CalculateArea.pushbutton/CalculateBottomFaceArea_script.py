import sys
import mastoron
import revitron
from revitron import _

selection = revitron.Selection().get()
if len(selection) < 1:
    sys.exit()

with revitron.Transaction():
    for element in revitron.Selection().get():
        faces = mastoron.FaceExtractor(element).getBottomFaces()
        area = 0
        for face in faces:
            area += face.Area
        _(element).set('Mass Area', area, 'Area')