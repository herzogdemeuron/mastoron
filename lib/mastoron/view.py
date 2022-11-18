import json
import revitron
from revitron import _
from collections import defaultdict
from mastoron.variables import NAME, SCHEME_NAME, VIEWS, MASTORON_VIEWS, MASTORON_COLORSCHEME


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
        self.affectedViews = revitron.DocumentConfigStorage().get(
            MASTORON_VIEWS, defaultdict())

    def load(self, colorScheme):
        """
        Loads all views affected by given color scheme.

        Args:
            colorScheme (dict): A color scheme
        """
        return self.affectedViews[colorScheme[NAME]]

    def save(self, colorScheme, viewId):
        """
        Saves a set of affected views to the revitron DocumentConfigStorage.

        Args:
            colorScheme (dict): A color scheme
            views (object): A set of Revit views
        """
        if not colorScheme[NAME] in self.affectedViews:
            self.affectedViews[colorScheme[NAME]] = [str(viewId)]

        else: 
            if not str(viewId) in self.affectedViews[colorScheme[NAME]]:
                self.affectedViews[colorScheme[NAME]].append(str(viewId))

        revitron.DocumentConfigStorage().set(MASTORON_VIEWS, self.affectedViews)

    def delete(self, colorScheme, viewId):
        """
        Removes an affected view from the revitron DocumentConfigStorage.

        Args:
            colorScheme (dict): A mastoron color scheme
            viewId (object or str): A Revit element id
        """
        self.affectedViews[colorScheme[NAME]].remove(str(viewId))
        if len(self.affectedViews[colorScheme[NAME]]) == 0:
            del self.affectedViews[colorScheme[NAME]]
            
        revitron.DocumentConfigStorage().set(MASTORON_VIEWS, self.affectedViews)


class AffectedElements:
    def __init__(self):
        pass

    @staticmethod
    def get(view):
        """
        Gets all Revit element ids of objects overridden by mastoron in given view.

        Args:
            view (object): A Revit view

        Returns:
            dict: {"<elementId>": "<nameOfColorScheme>", ... }
        """
        paramValue = _(view).get(MASTORON_COLORSCHEME)
        if paramValue:
            overriddenElements = json.loads(paramValue)
        else:
            overriddenElements = {}
        return overriddenElements

    @staticmethod
    def set(view, overriddenElements):
        """
        Saves the colorscheme override information for affected elements to a Revit view.

        Args:
            view (object): A Revit view
            elements (dict): {"<elementId>": "<nameOfColorScheme>", ... }
        """
        _(view).set(MASTORON_COLORSCHEME, json.dumps(overriddenElements))

    @staticmethod
    def filter(overriddenElements, scheme):
        """
        Filters a dictionary of affected elements for a given color scheme.

        Args:
            elements (dict): {"<elementId>": "<nameOfColorScheme>", ... }
            scheme (dict): A mastoron color scheme

        Returns:
            object: A list of Revit elements
        """
        viewElements = []
        for id, value in overriddenElements.items():
            if value == scheme[NAME]:
                elementId = revitron.DB.ElementId(int(id))
                element = revitron.DOC.GetElement(elementId)
                viewElements.append(element)
        
        return viewElements

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
        
    @staticmethod
    def delete(view, element):
        overriddenElements = AffectedElements.get(view)
        for id in overriddenElements.keys():
            if id == str(element.Id):
                del overriddenElements[id]
        
        AffectedElements.set(view, overriddenElements)
