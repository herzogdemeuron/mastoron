import revitron


class ElementOverrides:
    """
    Class for handling graphical element overrides.
    """
    def __init__(self, element):
        """
        Inits a new ElementOverrids instance.

        Args:
            element (object): A Revit element
        """
        self.overrides = revitron.DB.OverrideGraphicSettings()
        self.element = element
        self.id = element.Id

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
        revitron.DOC.ActiveView.SetElementOverrides(self.id, self.overrides)
        return self.element

    def clear(self):
        """
        Clears a graphical element overrides in view.
        """
        revitron.DOC.ActiveView.SetElementOverrides((self.id), self.overrides)
        return self.element