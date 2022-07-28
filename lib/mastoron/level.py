import revitron
from revitron import _


class Level:
    def __init__(self):
        pass

    @staticmethod
    def getLevelName(element, levels, min=True):
        """
        Gets the closest level to given object.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements

        Returns:
            string: The level name
        """
        levelName = Level._get(element, levels, _return='name', min=min)
        return levelName

    @staticmethod
    def getLevel(element, levels, min=True):
        """
        Gets the closest level to given object.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements

        Returns:
            object: The level
        """
        level = Level._get(element, levels, _return='element', min=min)
        return level

    @staticmethod
    def getDistance(element, levels, min=True):
        """
        Gets the closest level to given object.

        Args:
            element (object): Revit element
            levels (object): A list of Revit level elements

        Returns:
            float: The distance to the level
        """
        distance = Level._get(element, levels, _return='distance', min=min)
        return distance

    @staticmethod
    def _get(element, levels, _return, min=True):
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
        if min == True:
            z = _(element).getBbox().Min[2]
        if min == False:
            z = _(element).getBbox().Max[2]
        bestMatch = 99999.0
        levelMatch = None
        for level in levels:
            distance = abs(int(level.Elevation) - int(z))
            if int(bestMatch) > distance:
                levelMatch = level
                bestMatch = distance
        if _return == 'element':
            return levelMatch
        if _return == 'name':
            return levelMatch.Name
        if _return == 'distance':
            return bestMatch

