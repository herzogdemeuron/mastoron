import revitron
import colorsys
import os
import json
from collections import defaultdict


class Color:
    """
    Class for basic color operations.
    """

    def __init__(self):
        """
        Inits a new Color instance.
        """
        pass
    
    @staticmethod
    def HSVtoRGB(hsv):
        """
        Convert a color from hsv to rgb.

        Args:
            hsv (tuple): A color in hsv format.

        Returns:
            tuple: A color in rgb format
        """
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))

    @staticmethod
    def RGBtoHEX(rgb):
        return '%02x%02x%02x' % rgb

    @staticmethod
    def HEXtoRGB(hex):
        """
        Converts a hex color string to rgb.

        Args:
            hex (sting): The hex color

        Returns:
            tuple: The rgb color
        """
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


class ColorScheme:
    """
    Class for handling relationships between labels and colors.
    """

    JSON_PATH = 'C:\\temp\\mastoron\\colorscheme.json'

    def __init__(self):
        """
        Inits a new ColorScheme instance.
        """
        self.COLOR_SCHEMES = 'mastoron.colorschemes'
        self.schemes = revitron.DocumentConfigStorage().get(
            self.COLOR_SCHEMES, defaultdict())
        self.defaultColors = [
                            '#F44336', '#E91E63', '#9C27B0', '#673AB7',
                            '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4',
                            '#009688', '#4CAF50', '#8BC34A', '#CDDC39',
                            '#FFEB3B', '#FFC107', '#FF9800', '#FF5722',
                            '#795548', '#9E9E9E', '#607D8B'
                            ]
        self.additionalColors = [
                            '#D32F2F', '#C2185B', '#7B1FA2', '#512DA8',
                            '#303F9F', '#1976D2', '#0288D1', '#0097A7',
                            '#00796B', '#388E3C', '#689F38', '#AFB42B',
                            '#FBC02D', '#FFA000', '#F57C00', '#E64A19',
                            '#5D4037', '#616161', '#455A64'
                            ]
        self.extendedColors = self.defaultColors + self.additionalColors

    @staticmethod
    def showExcel(scheme, path=None):
        """
        Shows a color schme in excel.

        Args:
            scheme (dict): The color scheme
            path (string, optinal): The output file path. Defaults to None.
        """
        excel = ColorScheme.toExcel(scheme['data'], path)
        os.startfile(excel)

    @staticmethod
    def toJSON(data, path=JSON_PATH):
        """
        Write color scheme to json

        Args:
            data (dict): The data to export
            path (str, optional): The output file path. Defaults to 'C:\temp\mastoron\colorscheme.json'.

        Returns:
            string: The json file
        """
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w') as f:
            json.dump(data, f)

        return path

    @staticmethod
    def fromJSON(path):
        """
        Reads a color scheme from json.

        Args:
            path (string): The json file

        Returns:
            dict: The color scheme
        """
        with open(path, 'r') as f:
            scheme = json.load(f)

        return scheme

    def generate(self, schemeName, keys, excludeColors=None):
        """
        Generates a new color scheme.

        Args:
            schemeName (string): The name of the color scheme
            keys (string): A set of keys
            excludeColors (string, optional): A list of colors to exclude 

        Returns:
            dict: A color scheme: {name: schemeName, data: {key: color}}
        """
        colors = ColorScheme().getColors(len(keys), excludeColors)
        scheme = {}
        scheme['name'] = schemeName
        scheme['data'] = {}
        for value, color in zip(keys, colors):
            scheme['data'][value] = color
        return scheme

    def update(self, colorScheme, keys):
        """
        Updates a given color scheme with new keys and default colors.

        Args:
            colorScheme (dict): The color scheme to update
            keys (set): The keys to add

        Returns:
            dict: The updated color scheme
        """
        newkeys = set()
        for key in keys:
            if key not in colorScheme['data'].keys():
                newkeys.add(key)
        
        if newkeys:
            excludeColors = colorScheme['data'].values()
            tempScheme = ColorScheme().generate(
                'tempName', newkeys, excludeColors)
            if not tempScheme:
                return None
            colorScheme['data'].update(tempScheme['data'])

        return colorScheme

    def load(self, schemeName):
        """
        Loads a color scheme by name.

        Args:
            schemeName (string): The name of the color scheme

        Returns:
            dict: The color scheme
        """
        for scheme in self.schemes:
            if scheme['name'] == schemeName:
                return scheme
        return None

    def save(self, scheme):
        """
        Saves a color scheme to the revitron DocumentConfigStorage.

        Args:
            scheme (dict): A color scheme
        """
        writeSchemes = []
        update = False
        for existingScheme in self.schemes:
            if scheme['name'] == existingScheme['name']:
                existingScheme['data'] = scheme['data']
                update = True
            writeSchemes.append(existingScheme)
        
        if not update:
            writeSchemes.append(scheme)
        revitron.DocumentConfigStorage().set(self.COLOR_SCHEMES, writeSchemes)
    
    def getColors(self, count, excludeColors=None):
        import random
        totalCount = count
        if excludeColors:
            totalCount = count + len(excludeColors)

        if totalCount <= len(self.defaultColors):
            availableColors = self.defaultColors
        elif totalCount <= len(self.extendedColors):
            availableColors = self.extendedColors
        elif totalCount >= len(self.extendedColors) and totalCount < 100:
            hsvColors = ColorRange(count).getHSV()
            availableColors = []
            for hsvColor in hsvColors:
                rgbColor = Color.HSVtoRGB(hsvColor)
                hexColor = Color.RGBtoHEX(rgbColor)
                availableColors.append(hexColor)
        else:
            print('Too many keys, colors are indistiguishable.')
            return None

        if excludeColors:
            availableColors = filter(lambda color: color not in excludeColors, availableColors)

        colors = random.sample(availableColors, count)
        return colors

class ColorRange:
    """
    Class for working with color ranges.
    """
    def __init__(self, count, min=0, max=100):
        """
        Inits a new ColorRange instance.

        Accepted values::

            0 <= min < 100
            1 < max <= 100
            count < max - min

        """
        if 0 <= min and min < 100:
            self.min = min
        else:
            return None
        
        if 1 < max and max <= 100:
            self.max = max
        else:
            return None
            
        if count < max - min:
            self.count = count
        else:
            return None

        self.range = max - min

        if not self.count <= self.range:
            print('Count bigger than range.')
            return None

    def getHSV(self):
        """
        Gets a list of colors in hsv format.

        Returns:
            list: A list of hsv colors
        """
        hsv = []
        for i in [
                x * 0.01 for x in range(
                                        self.min,
                                        self.max,
                                            (self.range / self.count
                                            )
                                        )
                                    ]:
            hsv.append((i, 0.5, 0.9))
        return hsv

