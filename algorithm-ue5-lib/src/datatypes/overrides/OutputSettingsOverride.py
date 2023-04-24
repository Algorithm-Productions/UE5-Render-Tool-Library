from ..abstracts.UnrealOverride import UnrealOverride


class OutputSettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "autoVersion": ["auto_version", "bool"],
        "customEndFrame": ["custom_end_frame", "int"],
        "customStartFrame": ["custom_start_frame", "int"],
        "fileNameFormat": ["file_name_format", "str"],
        "frameNumberOffset": ["frame_number_offset", "int"],
        "handleFrameCount": ["handle_frame_count", "int"],
        "outputDirectory": ["output_directory", "path"],
        "outputFrameRate": ["output_frame_rate", "frameRate"],
        "outputFrameStep": ["output_frame_step", "int"],
        "outputResolutionX": ["output_resolution", "resolutionX"],
        "outputResolutionY": ["output_resolution", "resolutionY"],
        "overrideExistingOutput": ["override_existing_output", "bool"],
        "useCustomFrameRate": ["use_custom_frame_rate", "bool"],
        "useCustomPlaybackRange": ["use_custom_playback_range", "bool"],
        "versionNumber": ["version_number", "float"],
        "zeroPadFrameNumbers": ["zero_pad_frame_numbers", "int"]
    }
    UNREAL_SETTING_KEY = "output"

    def __init__(
            self,
            autoVersionFlag=False,
            customEndFrameFlag=False,
            customStartFrameFlag=False,
            fileNameFormatFlag=False,
            frameNumberOffsetFlag=False,
            handleFrameCountFlag=False,
            outputDirectoryFlag=False,
            outputFrameRateFlag=False,
            outputFrameStepFlag=False,
            outputResolutionXFlag=False,
            outputResolutionYFlag=False,
            overrideExistingOutputFlag=False,
            useCustomFrameRateFlag=False,
            useCustomPlaybackRangeFlag=False,
            versionNumberFlag=False,
            zeroPadFrameNumbersFlag=False
    ):
        self.autoVersionFlag = autoVersionFlag
        self.customEndFrameFlag = customEndFrameFlag
        self.customStartFrameFlag = customStartFrameFlag
        self.fileNameFormatFlag = fileNameFormatFlag
        self.frameNumberOffsetFlag = frameNumberOffsetFlag
        self.handleFrameCountFlag = handleFrameCountFlag
        self.outputDirectoryFlag = outputDirectoryFlag
        self.outputFrameRateFlag = outputFrameRateFlag
        self.outputFrameStepFlag = outputFrameStepFlag
        self.outputResolutionXFlag = outputResolutionXFlag
        self.outputResolutionYFlag = outputResolutionYFlag
        self.overrideExistingOutputFlag = overrideExistingOutputFlag
        self.useCustomFrameRateFlag = useCustomFrameRateFlag
        self.useCustomPlaybackRangeFlag = useCustomPlaybackRangeFlag
        self.versionNumberFlag = versionNumberFlag
        self.zeroPadFrameNumbersFlag = zeroPadFrameNumbersFlag

    @classmethod
    def from_dict(cls, data):
        autoVersionFlag = data["autoVersionFlag"] if (data and data["autoVersionFlag"]) else False
        customEndFrameFlag = data["customEndFrameFlag"] if (data and data["customEndFrameFlag"]) else False
        customStartFrameFlag = data["customStartFrameFlag"] if (data and data["customStartFrameFlag"]) else False
        fileNameFormatFlag = data["fileNameFormatFlag"] if (data and data["fileNameFormatFlag"]) else False
        frameNumberOffsetFlag = data["frameNumberOffsetFlag"] if (data and data["frameNumberOffsetFlag"]) else False
        handleFrameCountFlag = data["handleFrameCountFlag"] if (data and data["handleFrameCountFlag"]) else False
        outputDirectoryFlag = data["outputDirectoryFlag"] if (data and data["outputDirectoryFlag"]) else False
        outputFrameRateFlag = data["outputFrameRateFlag"] if (data and data["outputFrameRateFlag"]) else False
        outputFrameStepFlag = data["outputFrameStepFlag"] if (data and data["outputFrameStepFlag"]) else False
        outputResolutionXFlag = data["outputResolutionXFlag"] if (data and data["outputResolutionXFlag"]) else False
        outputResolutionYFlag = data["outputResolutionYFlag"] if (data and data["outputResolutionYFlag"]) else False
        overrideExistingOutputFlag = data["overrideExistingOutputFlag"] if \
            (data and data["overrideExistingOutputFlag"]) else False
        useCustomFrameRateFlag = data["useCustomFrameRateFlag"] if (data and data["useCustomFrameRateFlag"]) else False
        useCustomPlaybackRangeFlag = data["useCustomPlaybackRangeFlag"] if \
            (data and data["useCustomPlaybackRangeFlag"]) else False
        versionNumberFlag = data["versionNumberFlag"] if (data and data["versionNumberFlag"]) else False
        zeroPadFrameNumbersFlag = data["zeroPadFrameNumbersFlag"] if \
            (data and data["zeroPadFrameNumbersFlag"]) else False

        return cls(
            autoVersionFlag=autoVersionFlag,
            customEndFrameFlag=customEndFrameFlag,
            customStartFrameFlag=customStartFrameFlag,
            fileNameFormatFlag=fileNameFormatFlag,
            frameNumberOffsetFlag=frameNumberOffsetFlag,
            handleFrameCountFlag=handleFrameCountFlag,
            outputDirectoryFlag=outputDirectoryFlag,
            outputFrameRateFlag=outputFrameRateFlag,
            outputFrameStepFlag=outputFrameStepFlag,
            outputResolutionXFlag=outputResolutionXFlag,
            outputResolutionYFlag=outputResolutionYFlag,
            overrideExistingOutputFlag=overrideExistingOutputFlag,
            useCustomFrameRateFlag=useCustomFrameRateFlag,
            useCustomPlaybackRangeFlag=useCustomPlaybackRangeFlag,
            versionNumberFlag=versionNumberFlag,
            zeroPadFrameNumbersFlag=zeroPadFrameNumbersFlag
        )
