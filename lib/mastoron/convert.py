import revitron


class Convert:
    
    @staticmethod
    def toRevitElement(elementId):
        """
        Gets a Revit element by an id string.

        Args:
            elementId (string): A string representing a Revit element id

        Returns:
            object: A Revit element
        """
        revitId = revitron.DB.ElementId(int(elementId))
        return revitron.DOC.GetElement(revitId)