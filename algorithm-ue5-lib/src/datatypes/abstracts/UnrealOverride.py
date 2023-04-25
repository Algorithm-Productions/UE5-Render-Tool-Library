from abc import ABC

from .StorableProperty import StorableProperty


class UnrealOverride(ABC, StorableProperty):
    UNREAL_MAPPINGS = {}
    UNREAL_SETTING_KEY = ""

    @classmethod
    def changeUnreal(cls, config, flags, unrealObject):
        for key, val in config.items():
            if flags[key + "Flag"]:
                unrealKey, unrealType = cls.UNREAL_MAPPINGS[key][0], cls.UNREAL_MAPPINGS[key][1]
                if unrealType == "int":
                    unrealObject.updateProperty(int(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "float":
                    unrealObject.updateProperty(float(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "bool":
                    unrealObject.updateProperty(bool(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "str":
                    unrealObject.updateProperty(str(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "array":
                    unrealObject.updateArrayProperty(val, unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "map":
                    unrealObject.updateMapProperty(val, unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "path":
                    unrealObject.updatePathProperty(str(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "frameRate":
                    unrealObject.updateFrameRateProperty(int(val), unrealKey, cls.UNREAL_SETTING_KEY)
                elif unrealType == "resolutionX":
                    unrealObject.updateResolutionProperty(unrealKey, cls.UNREAL_SETTING_KEY, x=int(val), y=0)
                elif unrealType == "resolutionY":
                    unrealObject.updateResolutionProperty(unrealKey, cls.UNREAL_SETTING_KEY, y=int(val), x=0)
                elif unrealType == "aaMethod":
                    unrealObject.updateAAMethodProperty(str(val), unrealKey, cls.UNREAL_SETTING_KEY)
