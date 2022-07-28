import revitron
from revitron import _


class Extractor(object):
    """
    Base class for geometry extraction.
    """
    def __init__(self, element):
        """
        Inits a new Extractor instance.

        Args:
            element (object): A Revit Element
        """
        if isinstance(element, revitron.DB.Element):
            self.element = element
            self.geometry = _(element).getGeometry()
            self.solids = self.geometry.getSolids()
            self.faces = self.geometry.getFaces()
        elif isinstance(element, revitron.DB.Solid):
            self.solids = element
            self.faces = self.solids.Faces
        else:
            pass 


class FaceExtractor(Extractor):
    """
    A class for face extraction from elements or solids.
    """
    def __init__(self, element):
        """
        Inits a new FaceExtractor instance.

        Args:
            element (object): A Revit Element
        """
        super(FaceExtractor, self).__init__(element)    
    
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
    

class BorderExtractor(Extractor):
    """
    A class for edge extraction from faces.
    """
    def __init__(self, face):
        """
        Inits a new BorderExtractor instance.

        Args:
            element (object): A Revit face
        """
        if isinstance(face, revitron.DB.Face):
            self.face = face
        else:
            pass  
    
    def getBorder(self):
        """
        Gets the edges of a face as a curve loop.

        Args:
            face (object): A Revit face

        Returns:
            iList: A Revit curve loop
        """
        lines = self.face.GetEdgesAsCurveLoops()
        if len(lines) > 1:
            print('error')
            return None
        return lines[0]


class LineExtractor(Extractor):
    """
    A class for line extraction.
    """
    def __init__(self, element):
        """
        Inits a new LineExtractor instance.

        Args:
            element (object): A Revit family instance
        """
        super(LineExtractor, self).__init__(element)

    def bySubcategory(self, subcategory):
        """
        Gets all lines of specified subcategory inside an element.

        Args:
            subcategory (sting): The subcategory name

        Returns:
            object: The extracted curve loop
        """
        lines = self.geometry.getCurves()
        curveLoop = revitron.DB.CurveLoop()
        subcategoryLines = []
        for line in lines:
            if revitron.DOC.GetElement(line.GraphicsStyleId).Name == subcategory:
                subcategoryLines.append(line)
        count = 0
        for line in subcategoryLines:
            if count < len(subcategoryLines):
                try:
                    curveLoop.Append(line)
                    count += 1
                except:
                    try:
                        curveLoop.Append(line.CreateReversed())
                        count += 1
                    except:
                        pass
        
        if curveLoop.IsOpen():
            print('Cannot create floor for {}'.format(self.element.Id))
            return None

        return curveLoop
