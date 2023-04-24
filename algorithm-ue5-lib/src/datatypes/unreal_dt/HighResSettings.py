from ..abstracts.UnrealDataType import UnrealDataType


class HighResSettings(UnrealDataType):
    def __init__(
            self,
            burleySampleCount=0,
            overlapRatio=0.0,
            overrideSubSurfaceScattering=False,
            textureSharpnessBias=0.0,
            tileCount=0
    ):
        self.burleySampleCount = burleySampleCount
        self.overlapRatio = overlapRatio
        self.overrideSubSurfaceScattering = overrideSubSurfaceScattering
        self.textureSharpnessBias = textureSharpnessBias
        self.tileCount = tileCount

    @classmethod
    def from_dict(cls, data):
        burleySampleCount = data["burleySampleCount"] if (data and data["burleySampleCount"]) else 0
        overlapRatio = data["overlapRatio"] if (data and data["overlapRatio"]) else 0.0
        overrideSubSurfaceScattering = data["overrideSubSurfaceScattering"] if \
            (data and data["overrideSubSurfaceScattering"]) else False
        textureSharpnessBias = data["textureSharpnessBias"] if (data and data["textureSharpnessBias"]) else 0.0
        tileCount = data["tileCount"] if (data and data["tileCount"]) else 0

        return cls(
            burleySampleCount=burleySampleCount,
            overlapRatio=overlapRatio,
            overrideSubSurfaceScattering=overrideSubSurfaceScattering,
            textureSharpnessBias=textureSharpnessBias,
            tileCount=tileCount
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            burleySampleCount=unrealClass.burley_sample_count,
            overlapRatio=unrealClass.overlap_ratio,
            overrideSubSurfaceScattering=unrealClass.override_sub_surface_scattering,
            textureSharpnessBias=unrealClass.texture_sharpness_bias,
            tileCount=unrealClass.tile_count
        )
