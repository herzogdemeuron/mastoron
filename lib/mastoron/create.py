import mastoron
import revitron
from revitron import _
from variables import *
from System.Collections.Generic import List


class Creator(object):
    """
    Base class for creating Revit elements.
    """
    def __init__(self, docLevels, element, elementType):
        """
        Inits a new Creator instance.

        Args:
            docLevels (object): A list of Revit levels
            element (object): A Revit element
            elementType (object): A Revit element type
        """
        self.docLevels = docLevels
        self.element = element
        self.elementType = elementType


class FloorCreator(Creator):
    """
    Inits a new FloorCreator instance.
    """
    def __init__(self, docLevels, element, floorType, offset=0.0):
        super(FloorCreator, self).__init__(docLevels, element, floorType)
        self.offset = offset
    
    def fromBottomFaces(self):
        """
        Creates Revit floor objects from all downward facing faces of given element.

        Returns:
            object: A list of Revit floors
        """
        faces = mastoron.FaceExtractor(self.element).getBottomFaces()
        self.level = mastoron.Level.getLevel(
                                            self.element,
                                            self.docLevels,
                                            min=True
                                            )
        levelElevation = self.level.Elevation
        uv = revitron.DB.UV(0.5, 0.5)
        floors = []
        for face in faces:
            faceZ = face.Evaluate(uv).Z
            self.offset = faceZ - levelElevation
            self.curveLoop = mastoron.BorderExtractor(face).getBorder()
            floor = self._create()
            floors.append(floor)

        return floors

    def fromFamilyModelLines(self, subcategory):
        """
        Create a Revit floor object from model lines of a subcategory for given element.

        Args:
            subcategory (string): The name of a subcategory

        Returns:
            object: A Revit floor
        """
        self.curveLoop = mastoron.LineExtractor(self.element).bySubcategory(subcategory)
        self.level = mastoron.Level.getLevel(
                                            self.element,
                                            self.docLevels,
                                            min=True
                                            )
        levelElevation = self.level.Elevation
        if not self.curveLoop:
            return None
        if self.curveLoop.HasPlane:
            loopZ = self.curveLoop.GetPlane().Origin.Z
        else:
            print('Cannot create floor from non-planar lines.')
        self.offset = loopZ - levelElevation
        floor = self._create()

        return floor
    
    def fromTopFaces(self):
        """
        Create a Revit floor object from all upward facing faces of given element.

        Args:
            offset (float, optional): The offset distance. Defaults to 0.0.

        Returns:
            object: A list of Revit floor objects
        """
        faces = mastoron.FaceExtractor(self.element).getTopFaces()
        self.level = mastoron.Level.getLevel(
                                            self.element,
                                            self.docLevels,
                                            min=False
                                            )
        levelElevation = self.level.Elevation
        uv = revitron.DB.UV(0.5, 0.5)
        floors = []
        for face in faces:
            faceZ = face.Evaluate(uv).Z
            self.offset = faceZ - levelElevation
            self.curveLoop = mastoron.BorderExtractor(face).getBorder()
            floor = self._create()
            floors.append(floor)

        return floors


    def _create(self):
        """
        Internal function for creating a Revit floor.

        Returns:
            object: A Revit floor
        """
        if not self.curveLoop.IsCounterclockwise(revitron.DB.XYZ(0,0,1)):
            self.curveLoop.Flip()
        if not self.offset == 0.0:
                self.curveLoop = revitron.DB.CurveLoop.CreateViaOffset(
                                                    self.curveLoop,
                                                    offset,
                                                    revitron.DB.XYZ(0, 0, 1))
        self.curveLoop = List[revitron.DB.CurveLoop]([self.curveLoop])
        floor = revitron.DB.Floor.Create(
                                        revitron.DOC,
                                        self.curveLoop,
                                        self.elementType,
                                        self.level.Id
                                        )
        _(floor).set(FLOOR_OFFSET, self.offset)

        return floor


class WallCreator(Creator):
    """
    Inits a new WallCreator instance.
    """
    def __init__(self, docLevels, element, wallType):
        super(WallCreator, self).__init__(docLevels, element, wallType)

    def fromVerticalFaces(self):
        """
        Creates Revit wall objects from all vertical faces of given element.

        Returns:
            object: A list of Revit walls
        """
        faces = mastoron.FaceExtractor(self.element).getVeticalFaces()
        self.level = mastoron.Level.getLevel(
                                            self.element,
                                            self.docLevels,
                                            min=True
                                            )
        levelElevation = self.level.Elevation
        walls = []
        for face in faces:
            self.baseCurve = mastoron.BorderExtractor(face).getLowestEdge()
            self.topCurve = mastoron.BorderExtractor(face).getHighestEdge()
            faceMin = self.baseCurve.GetEndPoint(0)[2]
            if not round(faceMin, 5) == round(self.baseCurve.GetEndPoint(1)[2], 5):
                continue
            faceMax = self.topCurve.GetEndPoint(0)[2]
            offset = faceMin - levelElevation
            height = faceMax - faceMin
            wall = revitron.DB.Wall.Create(
                                        revitron.DOC,
                                        self.baseCurve,
                                        self.elementType,
                                        self.level.Id,
                                        height,
                                        offset,
                                        True,
                                        False
                                        )
            walls.append(wall)

        return walls


class RailingCreator(Creator):
    """
    Inits a new RailingCreator instance.
    """
    def __init__(self, docLevels, element, railingType):
        super(RailingCreator, self).__init__(docLevels, element, railingType)

    def fromTopFaces(self):
        """
        Creates a Revit railing objects from the boundaries of all upward facing faces of given element.

        Returns:
            object: A list of Revit railings
        """
        faces = mastoron.FaceExtractor(self.element).getTopFaces()
        self.level = mastoron.Level.getLevel(
                                            self.element,
                                            self.docLevels,
                                            min=False
                                            )
        levelElevation = self.level.Elevation
        uv = revitron.DB.UV(0.5, 0.5)
        railings = []
        for face in faces:
            faceZ = face.Evaluate(uv).Z
            self.offset = faceZ - levelElevation
            self.curveLoop = mastoron.BorderExtractor(face).getBorder()
            self.curveLoop = List[revitron.DB.CurveLoop]([self.curveLoop])
            railing = revitron.DB.Architecture.Railing.Create(
                                            document=revitron.DOC,
                                            curveLoop=self.curveLoop[0],
                                            railingTypeId=self.elementType,
                                            baseLevelId=self.level.Id
                                            )
            _(railing).set(BASE_OFFSET, self.offset)
            railings.append(railing)

        return railings