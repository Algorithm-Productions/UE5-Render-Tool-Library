from ..abstracts.UnrealOverride import UnrealOverride


class HighResSettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "burleySampleCount": ["burley_sample_count", "int"],
        "overlapRatio": ["overlap_ratio", "float"],
        "overrideSubSurfaceScattering": ["override_sub_surface_scattering", "bool"],
        "textureSharpnessBias": ["texture_sharpness_bias", "float"],
        "tileCount": ["tile_count", "int"]
    }
    UNREAL_SETTING_KEY = "highRes"

    def __init__(
            self,
            burleySampleCountFlag=False,
            overlapRatioFlag=False,
            overrideSubSurfaceScatteringFlag=False,
            textureSharpnessBiasFlag=False,
            tileCountFlag=False
    ):
        self.burleySampleCountFlag = burleySampleCountFlag
        self.overlapRatioFlag = overlapRatioFlag
        self.overrideSubSurfaceScatteringFlag = overrideSubSurfaceScatteringFlag
        self.textureSharpnessBiasFlag = textureSharpnessBiasFlag
        self.tileCountFlag = tileCountFlag

    @classmethod
    def from_dict(cls, data):
        burleySampleCountFlag = data["burleySampleCountFlag"] if (data and data["burleySampleCountFlag"]) else False
        overlapRatioFlag = data["overlapRatioFlag"] if (data and data["overlapRatioFlag"]) else False
        overrideSubSurfaceScatteringFlag = data["overrideSubSurfaceScatteringFlag"] if \
            (data and data["overrideSubSurfaceScatteringFlag"]) else False
        textureSharpnessBiasFlag = data["textureSharpnessBiasFlag"] if \
            (data and data["textureSharpnessBiasFlag"]) else False
        tileCountFlag = data["tileCountFlag"] if (data and data["tileCountFlag"]) else False

        return cls(
            burleySampleCountFlag=burleySampleCountFlag,
            overlapRatioFlag=overlapRatioFlag,
            overrideSubSurfaceScatteringFlag=overrideSubSurfaceScatteringFlag,
            textureSharpnessBiasFlag=textureSharpnessBiasFlag,
            tileCountFlag=tileCountFlag
        )
