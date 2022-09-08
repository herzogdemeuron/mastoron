import sys
import mastoron
import revitron
from mastoron.variables import NAME, DATA, IS_INSTANCE, PARAM_TYPE
from revitron import _


scheme = mastoron.ColorScheme.getFromUser()
if not scheme:
    sys.exit()

def clean(view, scheme):
    for viewId in mastoron.AffectedViews().load(scheme):
        viewElementId = revitron.DB.ElementId(int(viewId))
        view = revitron.DOC.GetElement(viewElementId)
        if view:
            overriddenElements = mastoron.AffectedElements.get(view)
            if len(overriddenElements) < 1:
                sys.exit()
            
            overriddenElements = mastoron.AffectedElements.filter(
                overriddenElements, scheme)

            cleaned = 0
            for element in overriddenElements:
                value = mastoron.GetKey(element,
                                        scheme[NAME],
                                        scheme[IS_INSTANCE],
                                        scheme[PARAM_TYPE])
                if value not in scheme[DATA]:
                    mastoron.ElementOverrides(view, element).clear()
                    mastoron.AffectedElements.delete(view, element)
                    cleaned += 1

            if len(overriddenElements) == cleaned:
                mastoron.AffectedViews().delete(scheme, viewId)
        else:
            mastoron.AffectedViews().delete(scheme, viewId)

affectedViews = None
try:
    affectedViews = mastoron.AffectedViews().load(scheme)
except:
    pass

if not affectedViews:
    with revitron.Transaction():
            mastoron.ColorScheme().delete(scheme)
else:
    with revitron.Transaction():
        usedSchemeKeys = set()
        for viewId in affectedViews:
            viewElementId = revitron.DB.ElementId(int(viewId))
            view = revitron.DOC.GetElement(viewElementId)
            if not view:
                continue
            overriddenElements = mastoron.AffectedElements.get(view)
            overriddenElements = mastoron.AffectedElements.filter(
                        overriddenElements, scheme)
            for element in overriddenElements:
                value = mastoron.GetKey(element,
                                        scheme[NAME],
                                        scheme[IS_INSTANCE],
                                        scheme[PARAM_TYPE])
                usedSchemeKeys.add(value)
        
        for key in scheme[DATA].keys():
            print(key)
            if key not in usedSchemeKeys:
                del scheme[DATA][key]

        if len(scheme[DATA]) >= 1:
            clean(view, scheme)
            mastoron.ColorScheme().save(scheme)
        else:
            clean(view, scheme)
            mastoron.ColorScheme().delete(scheme)

