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
    def __init__(self, docLevels, element, floorType):
        super(FloorCreator, self).__init__(docLevels, element, floorType)
    
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
    
    def _create(self):
        """
        Internal function for creating a Revit floor.

        Returns:
            object: A Revit floor
        """
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
            if not faceMin == self.baseCurve.GetEndPoint(1)[2]:
                continue
            faceMax = self.topCurve.GetEndPoint(0)[2]
            self.offset = faceMin - levelElevation
            wall = revitron.DB.Wall.Create(
                                        revitron.DOC,
                                        self.baseCurve,
                                        self.level.Id,
                                        False
                                        )
            _(wall).set(WALL_OFFSET, self.offset)
            height = faceMax - faceMin
            _(wall).set(WALL_HEIGHT, height)
            wall.Flip()
            walls.append(wall)
        return walls
