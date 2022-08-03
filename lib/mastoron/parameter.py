def ProcessOptions(elements):
    """
    Generates a list of all shared paramters from a given set of elements.
    The output of this function is intended to be used with the CommandSwitchWindow from pyRevit forms.

    Args:
        elements (object): A list of Revit elements

    Returns:
        string: A list of strings 
    """
    from collections import namedtuple
    ParamDef = namedtuple('ParamDef', ['name', 'type'])

    paramSets = []

    for el in elements:
        sharedParams = set()
        for param in el.ParametersMap:
            pdef = param.Definition
            sharedParams.add(ParamDef(pdef.Name, pdef.ParameterType))

        paramSets.append(sharedParams)

    if paramSets:
        allSharedParams = paramSets[0]
        for paramSet in paramSets[1:]:
            alSsharedParams = allSharedParams.intersection(paramSet)

        return {'{} <{}>'.format(x.name, x.type): x
                for x in allSharedParams}