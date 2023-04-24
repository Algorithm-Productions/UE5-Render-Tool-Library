from ..abstracts.UnrealOverride import UnrealOverride


class AASettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "aaMethod": ["anti_aliasing_method", "aaMethod"],
        "engineWarmUpCount": ["engine_warm_up_count", "int"],
        "overrideAAFlag": ["override_anti_aliasing", "bool"],
        "renderWarmUpCount": ["render_warm_up_count", "int"],
        "renderWarmUpFrames": ["render_warm_up_frames", "bool"],
        "spatialSampleCount": ["spatial_sample_count", "int"],
        "temporalSampleCount": ["temporal_sample_count", "int"],
        "useCameraCutForWarmUp": ["use_camera_cut_for_warm_up", "bool"]
    }
    UNREAL_SETTING_KEY = "aa"

    def __init__(
            self,
            aaMethodFlag=False,
            engineWarmUpCountFlag=False,
            overrideAAFlag=False,
            renderWarmUpCountFlag=False,
            renderWarmUpFramesFlag=False,
            spatialSampleCountFlag=False,
            temporalSampleCountFlag=False,
            useCameraCutForWarmUpFlag=False
    ):
        self.aaMethodFlag = aaMethodFlag
        self.engineWarmUpCountFlag = engineWarmUpCountFlag
        self.overrideAAFlag = overrideAAFlag
        self.renderWarmUpCountFlag = renderWarmUpCountFlag
        self.renderWarmUpFramesFlag = renderWarmUpFramesFlag
        self.spatialSampleCountFlag = spatialSampleCountFlag
        self.temporalSampleCountFlag = temporalSampleCountFlag
        self.useCameraCutForWarmUpFlag = useCameraCutForWarmUpFlag

    @classmethod
    def from_dict(cls, data):
        aaMethodFlag = data["aaMethodFlag"] if (data and data["aaMethodFlag"]) else False
        engineWarmUpCountFlag = data["engineWarmUpCountFlag"] if (data and data["engineWarmUpCountFlag"]) else False
        overrideAAFlag = data["overrideAAFlag"] if (data and data["overrideAAFlag"]) else False
        renderWarmUpCountFlag = data["renderWarmUpCountFlag"] if (data and data["renderWarmUpCountFlag"]) else False
        renderWarmUpFramesFlag = data["renderWarmUpFramesFlag"] if (data and data["renderWarmUpFramesFlag"]) else False
        spatialSampleCountFlag = data["spatialSampleCountFlag"] if (data and data["spatialSampleCountFlag"]) else False
        temporalSampleCountFlag = data["temporalSampleCountFlag"] if \
            (data and data["temporalSampleCountFlag"]) else False
        useCameraCutForWarmUpFlag = data["useCameraCutForWarmUpFlag"] if \
            (data and data["useCameraCutForWarmUpFlag"]) else False

        return cls(
            aaMethodFlag=aaMethodFlag,
            engineWarmUpCountFlag=engineWarmUpCountFlag,
            overrideAAFlag=overrideAAFlag,
            renderWarmUpCountFlag=renderWarmUpCountFlag,
            renderWarmUpFramesFlag=renderWarmUpFramesFlag,
            spatialSampleCountFlag=spatialSampleCountFlag,
            temporalSampleCountFlag=temporalSampleCountFlag,
            useCameraCutForWarmUpFlag=useCameraCutForWarmUpFlag
        )
