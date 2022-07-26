import revitron
from revitron import _


class Level:
    def __init__(self):
        pass

    @staticmethod
    def getLevelName(element, levels):
        """
        Gets the closest level to given object.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements

        Returns:
            string: The level name
        """
        levelName = Level._get(element, levels, _return='name')
        return levelName

    @staticmethod
    def getLevel(element, levels):
        """
        Gets the closest level to given object.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements

        Returns:
            object: The level
        """
        level = Level._get(element, levels, _return='element')
        return level

    @staticmethod
    def _get(element, levels, _return):
        """
        Performs a geometrical test to determine the closest level for the
        element's bounding box z-min.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements
            _return (string): Returntype: 'element', 'name'

        Returns:
            varied: The level element, the level name
        """
        zMin = _(element).getBbox().Min[2]
        bestMatch = 99999
        levelMatch = None
        for level in levels:
            distance = abs(int(level.Elevation) - int(zMin))
            if int(bestMatch) > distance:
                levelMatch = level
                bestMatch = distance
        if _return == 'element':
            return levelMatch
        if _return == 'name':
            return levelMatch.Name

