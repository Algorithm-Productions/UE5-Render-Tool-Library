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
                    unrealObject.updateProperty(cls.UNREAL_SETTING_KEY, unrealKey, int(val))
                elif unrealType == "float":
                    unrealObject.updateProperty(cls.UNREAL_SETTING_KEY, unrealKey, float(val))
                elif unrealType == "bool":
                    unrealObject.updateProperty(cls.UNREAL_SETTING_KEY, unrealKey, bool(val))
                elif unrealType == "str":
                    unrealObject.updateProperty(cls.UNREAL_SETTING_KEY, unrealKey, str(val))
                elif unrealType == "array":
                    unrealObject.updateArrayProperty(cls.UNREAL_SETTING_KEY, unrealKey, val)
                elif unrealType == "map":
                    unrealObject.updateMapProperty(cls.UNREAL_SETTING_KEY, unrealKey, val)
                elif unrealType == "path":
                    unrealObject.updatePathProperty(cls.UNREAL_SETTING_KEY, unrealKey, str(val))
                elif unrealType == "frameRate":
                    unrealObject.updateFrameRateProperty(cls.UNREAL_SETTING_KEY, unrealKey, int(val))
                elif unrealType == "resolutionX":
                    unrealObject.updateResolutionProperty(cls.UNREAL_SETTING_KEY, unrealKey, x=int(val), y=0)
                elif unrealType == "resolutionY":
                    unrealObject.updateResolutionProperty(cls.UNREAL_SETTING_KEY, unrealKey, y=int(val), x=0)
                elif unrealType == "aaMethod":
                    unrealObject.updateAAMethodProperty(cls.UNREAL_SETTING_KEY, unrealKey, str(val))
