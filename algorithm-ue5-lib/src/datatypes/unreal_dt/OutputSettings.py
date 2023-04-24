from ..abstracts.UnrealDataType import UnrealDataType


class OutputSettings(UnrealDataType):
    def __init__(
            self,
            autoVersion=False,
            customEndFrame=0,
            customStartFrame=0,
            fileNameFormat='',
            frameNumberOffset=0,
            handleFrameCount=0,
            outputDirectory='',
            outputFrameRate=0,
            outputFrameStep=0,
            outputResolutionX=0,
            outputResolutionY=0,
            overrideExistingOutput=False,
            useCustomFrameRate=False,
            useCustomPlaybackRange=False,
            versionNumber=0,
            zeroPadFrameNumbers=0
    ):
        self.autoVersion = autoVersion
        self.customEndFrame = customEndFrame
        self.customStartFrame = customStartFrame
        self.fileNameFormat = fileNameFormat
        self.frameNumberOffset = frameNumberOffset
        self.handleFrameCount = handleFrameCount
        self.outputDirectory = outputDirectory
        self.outputFrameRate = outputFrameRate
        self.outputFrameStep = outputFrameStep
        self.outputResolutionX = outputResolutionX
        self.outputResolutionY = outputResolutionY
        self.overrideExistingOutput = overrideExistingOutput
        self.useCustomFrameRate = useCustomFrameRate
        self.useCustomPlaybackRange = useCustomPlaybackRange
        self.versionNumber = versionNumber
        self.zeroPadFrameNumbers = zeroPadFrameNumbers

    @classmethod
    def from_dict(cls, data):
        autoVersion = data["autoVersion"] if (data and data["autoVersion"]) else False
        customEndFrame = data["customEndFrame"] if (data and data["customEndFrame"]) else 0
        customStartFrame = data["customStartFrame"] if (data and data["customStartFrame"]) else 0
        fileNameFormat = data["fileNameFormat"] if (data and data["fileNameFormat"]) else ''
        frameNumberOffset = data["frameNumberOffset"] if (data and data["frameNumberOffset"]) else 0
        handleFrameCount = data["handleFrameCount"] if (data and data["handleFrameCount"]) else 0
        outputDirectory = data["outputDirectory"] if (data and data["outputDirectory"]) else ''
        outputFrameRate = data["outputFrameRate"] if (data and data["outputFrameRate"]) else 0
        outputFrameStep = data["outputFrameStep"] if (data and data["outputFrameStep"]) else 0
        outputResolutionX = data["outputResolutionX"] if (data and data["outputResolutionX"]) else 0
        outputResolutionY = data["outputResolutionY"] if (data and data["outputResolutionY"]) else 0
        overrideExistingOutput = data["overrideExistingOutput"] if (data and data["overrideExistingOutput"]) else False
        useCustomFrameRate = data["useCustomFrameRate"] if (data and data["useCustomFrameRate"]) else False
        useCustomPlaybackRange = data["useCustomPlaybackRange"] if (data and data["useCustomPlaybackRange"]) else False
        versionNumber = data["versionNumber"] if (data and data["versionNumber"]) else 0
        zeroPadFrameNumbers = data["zeroPadFrameNumbers"] if (data and data["zeroPadFrameNumbers"]) else 0

        return cls(
            autoVersion=autoVersion,
            customEndFrame=customEndFrame,
            customStartFrame=customStartFrame,
            fileNameFormat=fileNameFormat,
            frameNumberOffset=frameNumberOffset,
            handleFrameCount=handleFrameCount,
            outputDirectory=outputDirectory,
            outputFrameRate=outputFrameRate,
            outputFrameStep=outputFrameStep,
            outputResolutionX=outputResolutionX,
            outputResolutionY=outputResolutionY,
            overrideExistingOutput=overrideExistingOutput,
            useCustomFrameRate=useCustomFrameRate,
            useCustomPlaybackRange=useCustomPlaybackRange,
            versionNumber=versionNumber,
            zeroPadFrameNumbers=zeroPadFrameNumbers
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            autoVersion=unrealClass.auto_version,
            customEndFrame=unrealClass.custom_end_frame,
            customStartFrame=unrealClass.custom_start_frame,
            fileNameFormat=unrealClass.file_name_format,
            frameNumberOffset=unrealClass.frame_number_offset,
            handleFrameCount=unrealClass.handle_frame_count,
            outputDirectory=unrealClass.output_directory.path,
            outputFrameRate=unrealClass.output_frame_rate.numerator,
            outputFrameStep=unrealClass.output_frame_step,
            outputResolutionX=unrealClass.output_resolution.x,
            outputResolutionY=unrealClass.output_resolution.y,
            overrideExistingOutput=unrealClass.override_existing_output,
            useCustomFrameRate=unrealClass.use_custom_frame_rate,
            useCustomPlaybackRange=unrealClass.use_custom_playback_range,
            versionNumber=unrealClass.version_number,
            zeroPadFrameNumbers=unrealClass.zero_pad_frame_numbers
        )
