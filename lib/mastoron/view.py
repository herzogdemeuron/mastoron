import revitron
import mastoron
from revitron import _
from collections import defaultdict
from variables import NAME, MASTORON_VIEWS


class ElementOverrides:
    """
    Class for handling graphical element overrides.
    """
    def __init__(self, view, element):
        """
        Inits a new ElementOverrids instance.

        Args:
            element (object): A Revit element
        """
        self.overrides = revitron.DB.OverrideGraphicSettings()
        self.element = element
        self.id = element.Id
        self.view = view

    def set(self, color, patternId, overrideCutPattern=True):
        """
        Sets graphical element overrides in the active view.

        Args:
            color (int): A list or tuple (r, g, b)
            pattern (object): An element id of a Revit fill pattern
            overrideCutPattern (bool, optional): Override cut pattern. Defaults to True.
        """
        patternColor = revitron.DB.Color(color[0], color[1], color[2])
        x = 0.7
        lineColor =  revitron.DB.Color(color[0] * x, color[1] * x, color[2] * x)
        self.overrides.SetSurfaceForegroundPatternColor(patternColor)
        self.overrides.SetSurfaceForegroundPatternId(patternId)
        self.overrides.SetProjectionLineColor(lineColor)
        if overrideCutPattern:
            self.overrides.SetCutForegroundPatternColor(patternColor)
            self.overrides.SetCutForegroundPatternId(patternId)
        self.view.SetElementOverrides(self.id, self.overrides)
        return self.element

    def clear(self):
        """
        Clears a graphical element overrides in view.
        """
        self.view.SetElementOverrides((self.id), self.overrides)
        return self.element


class AffectedViews:
    """
    Class for handling views affected by mastoron.
    """

    def __init__(self):
        self.affectedViews = mastoron.ConfigStorage().get(
            MASTORON_VIEWS, defaultdict())

    def delete(self, colorScheme, viewId):
        """
        Removes an affected view from the revitron DocumentConfigStorage.

        Args:
            colorScheme (dict): A mastoron color scheme
            viewId (object or str): A Revit element id
        """
        del self.affectedViews[colorScheme[NAME]][str(viewId)]
        if len(self.affectedViews[colorScheme[NAME]]) == 0:
            del self.affectedViews[colorScheme[NAME]]
            
        mastoron.ConfigStorage().set(MASTORON_VIEWS, self.affectedViews)

    def get(self, colorScheme):
        return self.affectedViews[colorScheme[NAME]]


class AffectedElements:
    """
    Class for handling elements affected by mastoron.
    """

    def __init__(self):
        self.affectedViews = mastoron.ConfigStorage().get(
            MASTORON_VIEWS, defaultdict())

    def get(self, colorScheme, viewId=None):
        """
        Gets all Revit element ids of objects overridden by mastoron.

        Returns::

            If a viewId was provided a list of element ids.
            if no viewId was provided a dict of view ids with the ids of 
            overridden elements.

        Args:
            colorScheme (dict): A mastoron colorScheme
            viewId (Id or string, optional): A Revit element Id. Defaults to None.

        Returns:
            mixed: dict or list
        """
        if not colorScheme[NAME] in self.affectedViews:
            self.affectedViews[colorScheme[NAME]] = {}

        schemeViews = self.affectedViews[colorScheme[NAME]]
        if viewId:
            if not str(viewId) in schemeViews:
                schemeViews[str(viewId)] = []

            return schemeViews[str(viewId)]
        else:
            return schemeViews

    def dump(self, colorScheme, viewId, overriddenElements):
        """
        Saves the colorscheme override information for affected elements to 
        the Revitron document config.

        Args:
            colorScheme (dict): A mastoron color scheme
            viewId (element id or string): A Revit element id
            overriddenElements (string): A list of Revit element ids
        """
        if not colorScheme[NAME] in self.affectedViews:
            self.affectedViews[colorScheme[NAME]] = {}
        
        overriddenElements = [str(x) for x in set(overriddenElements)]
        self.affectedViews[colorScheme[NAME]][str(viewId)] = overriddenElements
        mastoron.ConfigStorage().set(MASTORON_VIEWS, self.affectedViews)

    @staticmethod
    def purge(view, scheme):
        """
        Deletes all overriddenElements for given color scheme stored in 
        the mastoron config of given view.

        Args:
            view (object): A Revit view
            scheme (dict): A mastoron color scheme
        """
        overriddenElements = AffectedElements.get(view)
        for id, value in overriddenElements.items():
            if value == scheme[NAME]:
                del overriddenElements[id]
        
        AffectedElements.set(view, overriddenElements)
        
    def delete(self, colorScheme, viewId, elementId):
        self.affectedViews[colorScheme[NAME]][str(viewId)].remove(str(elementId))
        if len(self.affectedViews[colorScheme[NAME]][str(viewId)]) == 0:
            del self.affectedViews[colorScheme[NAME]][str(viewId)]

        mastoron.ConfigStorage().set(MASTORON_VIEWS, self.affectedViews)
        
