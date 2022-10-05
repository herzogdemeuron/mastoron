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
        """
        Gets the lowest face in a list of Revit faces.

        Returns:
            object: A Revit face
        """
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
        """
        Gets all downward facing faces in a list of Revit faces.

        Returns:
            object: A list of Revit faces
        """
        bottomFaces = self._getFaces(revitron.DB.XYZ(0, 0, -1))
        return bottomFaces

    def getTopFace(self):
        """
        Get the highest face in a list of Revit faces.

        Returns:
            object: A Revit face
        """
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
        """
        Get all upward facing faces in a list of Reevit faces.

        Returns:
            object: A list of Revit faces
        """
        topFaces = self._getFaces(revitron.DB.XYZ(0, 0, 1))
        return topFaces

    def getVeticalFaces(self):
        """
        Get all vertical faces in a list of Revit faces.

        Returns:
            object: A list of Revit faces
        """
        verticalFaces = []
        for face in self.faces:
            normal = face.ComputeNormal(revitron.DB.UV(0.5, 0.5))
            dotProduct = normal.DotProduct(revitron.DB.XYZ(0, 0, 1))
            if dotProduct == 0:
                verticalFaces.append(face)

        return verticalFaces

    def _getFaces(self, vector):
        """
        Internal function for getting faces by their normal vector.

        Args:
            vector (object): A Revit XYZ object

        Returns:
            object: A list of Revit faces
        """
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

    def getLowestEdge(self):
        """
        Gets the lowest edge from a face.

        Returns:
            object: A Revit curve
        """
        curves = self.getBorder()
        selectedCurve = None
        selectedPoint = 999999999
        for curve in curves:
            point = curve.Evaluate(0.5, True)
            if point[2] < selectedPoint:
                selectedPoint = point[2]
                selectedCurve = curve

        return selectedCurve

    def getHighestEdge(self):
        """
        Gets the highest edge from a face.

        Returns:
            object: A Revit curve
        """
        curves = self.getBorder()
        selectedCurve = None
        selectedPoint = -999999999
        for curve in curves:
            point = curve.Evaluate(0.5, True)
            if point[2] > selectedPoint:
                selectedPoint = point[2]
                selectedCurve = curve

        return selectedCurve

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
