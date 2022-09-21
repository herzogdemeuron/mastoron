import revitron
from revitron import _
from .variables import NAME
from .variables import ROUNDING_DECIMALS

def ProcessOptions(elements, staticParams=None):
    """
    Generates a list of all shared paramters from a given set of elements.
    The output of this function is intended to be used with the CommandSwitchWindow from pyRevit forms.

    Args:
        elements (object): A list of Revit elements

    Returns:
        dict: A list of strings 
    """
    from collections import namedtuple
    ParamDef = namedtuple('ParamDef', ['name', 'type', 'isInstance'])

    paramSets = []

    for el in elements:
        typeId = el.GetTypeId()
            
        sharedParams = set()
        for param in el.ParametersMap:
            pdef = param.Definition
            sharedParams.add(ParamDef(pdef.Name, pdef.ParameterType, True))

        elType = revitron.DOC.GetElement(typeId)
        if elType:
            for param in elType.ParametersMap:
                pdef = param.Definition
                sharedParams.add(ParamDef(pdef.Name, pdef.ParameterType, False))

        paramSets.append(sharedParams)

    if paramSets:
        allSharedParams = paramSets[0]
        for paramSet in paramSets[1:]:
            allSharedParams = allSharedParams.intersection(paramSet)

        if staticParams:
            allStaticParams = set()
            for paramSet in paramSets:
                for param in paramSet:
                    if param.name in staticParams:
                        allStaticParams.add(param)
            allSharedParams = allSharedParams | allStaticParams
        
        return {'{}'.format(x.name): x for x in allSharedParams}


def GetKey(element, parameter, isInstance, type):
    """
    Gets the value of given parameter from either the given element or its type.

    Args:
        element (object): A Revit element
        parameter (string): The name of the parameter
        isInstance (bool): True for instance parameters, False for type parameters
        type (string): The type of the parameter (Area, Number, Length, etc...)

    Returns:
        string: The value of the parameter
    """
    if isInstance:
        key = _(element).get(parameter)
    elif not isInstance:
        key = _(revitron.DOC.GetElement(element.GetTypeId())).get(parameter)
    if not key:
        return None
    if not isinstance(key, int):
        if str(type) == 'Invalid':
            if not _(key).getClassName() == 'ElemntId':
                return None
            key = _(revitron.DOC.GetElement(key)).get(NAME)
    try:
        key = str(round(key, ROUNDING_DECIMALS))
    except:
        key = str(key)
    return key