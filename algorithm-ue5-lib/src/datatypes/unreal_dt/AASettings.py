from ..abstracts.UnrealDataType import UnrealDataType


class AASettings(UnrealDataType):
    def __init__(
            self,
            aaMethod='',
            engineWarmUpCount=0,
            overrideAA=False,
            renderWarmUpCount=0,
            renderWarmUpFrames=False,
            spatialSampleCount=0,
            temporalSampleCount=0,
            useCameraCutForWarmUp=False
    ):
        self.aaMethod = aaMethod
        self.engineWarmUpCount = engineWarmUpCount
        self.overrideAA = overrideAA
        self.renderWarmUpCount = renderWarmUpCount
        self.renderWarmUpFrames = renderWarmUpFrames
        self.spatialSampleCount = spatialSampleCount
        self.temporalSampleCount = temporalSampleCount
        self.useCameraCutForWarmUp = useCameraCutForWarmUp

    @classmethod
    def from_dict(cls, data):
        aaMethod = data["aaMethod"] if (data and data["aaMethod"]) else ''
        engineWarmUpCount = data["engineWarmUpCount"] if (data and data["engineWarmUpCount"]) else 0
        overrideAA = data["overrideAA"] if (data and data["overrideAA"]) else False
        renderWarmUpCount = data["renderWarmUpCount"] if (data and data["renderWarmUpCount"]) else 0
        renderWarmUpFrames = data["renderWarmUpFrames"] if (data and data["renderWarmUpFrames"]) else False
        spatialSampleCount = data["spatialSampleCount"] if (data and data["spatialSampleCount"]) else 0
        temporalSampleCount = data["temporalSampleCount"] if (data and data["temporalSampleCount"]) else 0
        useCameraCutForWarmUp = data["useCameraCutForWarmUp"] if (data and data["useCameraCutForWarmUp"]) else False

        return cls(
            aaMethod=aaMethod,
            engineWarmUpCount=engineWarmUpCount,
            overrideAA=overrideAA,
            renderWarmUpCount=renderWarmUpCount,
            renderWarmUpFrames=renderWarmUpFrames,
            spatialSampleCount=spatialSampleCount,
            temporalSampleCount=temporalSampleCount,
            useCameraCutForWarmUp=useCameraCutForWarmUp
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            aaMethod=str(unrealClass.anti_aliasing_method),
            engineWarmUpCount=unrealClass.engine_warm_up_count,
            overrideAA=unrealClass.override_anti_aliasing,
            renderWarmUpCount=unrealClass.render_warm_up_count,
            renderWarmUpFrames=unrealClass.render_warm_up_frames,
            spatialSampleCount=unrealClass.spatial_sample_count,
            temporalSampleCount=unrealClass.temporal_sample_count,
            useCameraCutForWarmUp=unrealClass.use_camera_cut_for_warm_up
        )
