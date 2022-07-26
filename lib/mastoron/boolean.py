import revitron
import mastoron
from revitron import _
from System.Collections.Generic import List


class BooleanSketchBased(object):
    """
    Base class for boolean operations on sketch based elements.
    """
    def __init__(self, elements):
        """
        Inits a new BooleaSketchBased instance.

        Args:
            elements (object): A list of Revit elements
        """
        filter = revitron.Filter()
        levels = filter.byCategory('Levels').noTypes().getElements()
        intersections = self.getIntersects(elements)
        idStrings = self.toIdString(intersections)
        groups = self.mergeLists(idStrings)
        groups = self.toElements(groups)
        self.newElements = []
        for group in groups:
            newSolid = self.makeBoolean(group)
            face = mastoron.Extractor(newSolid).getBottomFace()
            level = mastoron.Level.getLevel(group[0], levels)
            curveLoop = self.getCurveLoop(face)
            self.newElements.append({'loop': curveLoop, 'level': level})

    def getIntersects(self, elements):
        """
        Gets all intersecting elements for each input element.

        Args:
            elements (object): A list of Revit elements 

        Returns:
            object: A list of lists containing the intersecting elements
        """
        groups = []
        for element in elements:
            group = [element]
            for intersected in revitron.Filter().byIntersection(element).getElements():
                group.append(intersected)
            
            groups.append(group)
        return groups

    def toIdString(self, nestedList):
        """
        Convert Revit elements to element ids as strings.

        Args:
            nestedList (object): A list of lists of Revit elements

        Returns:
            string: A list of lists of element ids as strings
        """
        out = []
        for list in nestedList:
            ids = []
            for item in list:
                ids.append(str(item.Id))
            out.append(ids)
        return out

    def toElements(self, nestedList):
        """
        Converts strings of element ids to revit elements.

        Args:
            nestedList (string): A list of lists of element ids as strings

        Returns:
            object: A list of lists of Revit elements
        """
        out = []
        for list in nestedList:
            elements = []
            for item in list:
                id = revitron.DB.ElementId(int(item))
                elements.append(revitron.DOC.GetElement(id))
            out.append(elements)
        return out

    def mergeLists(self, lists):
        """
        Combines all lists with shared items into one list.
        List that do not share items will remain separate.

        Args:
            lists (string): A list of lists containing strings

        Returns:
            string: A list of lists with no shared items inbetween lists
        """
        out = []
        while len(lists)>0:
            first, rest = lists[0], lists[1:]
            first = set(first)

            lf = -1
            while len(first)>lf:
                lf = len(first)

                rest2 = []
                for r in rest:
                    if len(first.intersection(set(r)))>0:
                        first |= set(r)
                    else:
                        rest2.append(r)     
                rest = rest2
            out.append(list(first))
            lists = rest
        return out

    def makeBoolean(self, elements):
        """
        Performs a boolean union operation on a list of solids.

        Args:
            elements (solid): A list of Revit solids

        Returns:
            solid: The resulting solid
        """
        newSolid = _(elements[0]).getGeometry().getSolids()[0]
        boolType = revitron.DB.BooleanOperationsType.Union
        BooleanOperationsUtils = revitron.DB.BooleanOperationsUtils
        for element in elements[1:]:
            solid = _(element).getGeometry().getSolids()[0]
            newSolid = BooleanOperationsUtils.ExecuteBooleanOperation(
                                                                newSolid,
                                                                solid,
                                                                boolType
                                                                )
        return newSolid


    def getCurveLoop(self, face):
        """
        Gets the edges of a face as a curve loop.

        Args:
            face (object): A Revit face

        Returns:
            iList: A Revit curve loop
        """
        lines = face.GetEdgesAsCurveLoops()
        if len(lines) > 1:
            print('error')
            return None
        iList = List[revitron.DB.CurveLoop]([lines[0]])
        return iList


class BooleanFloors(BooleanSketchBased):
    """
    Class for boolean operations on floor elements.
    """
    def __init__(self, floors, floorType):
        """
        Inits a new BooleanFloor instance that booleans all input floors.
        Deletes input floors.

        Args:
            floors (object): A list of Revit floors
            floorType (object): A Revit floor type
        """
        super(BooleanFloors, self).__init__(floors)
        for element in self.newElements:
            revitron.DB.Floor.Create(
                                    revitron.DOC,
                                    element['loop'],
                                    floorType,
                                    element['level'].Id
                                    )
        for item in floors:
            _(item).delete()


class BooleanRoof(BooleanSketchBased):
    def __init__(self):
        super().__init__()


class BooleanCeiling(BooleanSketchBased):
    def __init__(self):
        super().__init__()