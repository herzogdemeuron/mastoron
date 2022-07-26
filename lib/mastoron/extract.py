import mastoron
import revitron
from revitron import _


class Extractor:
    """
    A class for geometry extraction from elements or solids
    """
    def __init__(self, element):
        """
        Inits a new Extractor instance.

        Args:
            element (object): A Revit Element
        """
        if isinstance(element, revitron.DB.Element):
            self.geometry = _(element).getGeometry()
            self.solids = self.geometry.getSolids()
            self.faces = self.geometry.getFaces()
        elif isinstance(element, revitron.DB.Solid):
            self.solids = element
            self.faces = self.solids.Faces
        else:
            pass        
    
    def getBottomFace(self):
        selectedFace = None
        selectedPoint = 999999999
        for face in self.faces:
            uv = revitron.DB.UV(0.5, 0.5)
            point = face.Evaluate(uv)
            if point[2] < selectedPoint:
                selectedPoint = point
                selectedFace = face
        return selectedFace

    def getBottomFaces(self):
        bottomFaces = self._getFaces(revitron.DB.XYZ(0, 0, -1))
        return bottomFaces

    def getTopFace(self):
        selectedFace = None
        selectedPoint = -999999999
        for face in self.faces:
            uv = revitron.DB.UV(0.5, 0.5)
            point = face.Evaluate(uv)
            if point[2] > selectedPoint:
                selectedPoint = point
                selectedFace = face
        return selectedFace

    def getTopFaces(self):
        topFaces = self._getFaces(revitron.DB.XYZ(0, 0, 1))
        return topFaces

    def _getFaces(self, vector):
        faces = []
        for face in self.faces:
            normal = face.ComputeNormal(revitron.DB.UV(0.5, 0.5))
            if normal.IsAlmostEqualTo(vector):
                faces.append(face)
        return faces
    