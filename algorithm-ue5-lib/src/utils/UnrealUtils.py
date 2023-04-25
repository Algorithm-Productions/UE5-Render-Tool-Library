from datetime import datetime
import os

import unreal

from ..datatypes import RenderSettings
from ..datatypes.overrides import AASettingsOverride, ConsoleSettingsOverride, HighResSettingsOverride, \
    OutputSettingsOverride
from ..datatypes.unreal_dt import AASettings, ConsoleSettings, HighResSettings, OutputSettings


def buildArray(array):
    returnArray = unreal.Array(str)
    for item in array:
        returnArray.append(item)

    return returnArray


def buildMap(givenMap):
    returnMap = {}
    for key, val in givenMap.items():
        returnMap[key] = float(val)

    return returnMap


def checkOutputType(setting):
    if type(setting) == unreal.MoviePipelineImageSequenceOutput_BMP:
        return "BMP"
    elif type(setting) == unreal.MoviePipelineImageSequenceOutput_EXR:
        return "EXR"
    elif type(setting) == unreal.MoviePipelineImageSequenceOutput_JPG:
        return "JPG"
    elif type(setting) == unreal.MoviePipelineImageSequenceOutput_PNG:
        return "PNG"
    else:
        return ''


def checkRenderType(setting):
    if type(setting) == unreal.MoviePipelineDeferredPassBase:
        return "Deferred Rendering (Base)"
    elif type(setting) == unreal.MoviePipelineDeferredPass_PathTracer:
        return "Path Tracer"
    elif type(setting) == unreal.MoviePipelineDeferredPass_DetailLighting:
        return "Deferred Rendering (Detail Lighting)"
    elif type(setting) == unreal.MoviePipelineDeferredPass_LightingOnly:
        return "Deferred Rendering (Lighting Only)"
    elif type(setting) == unreal.MoviePipelineDeferredPass_ReflectionsOnly:
        return "Deferred Rendering (Reflections Only)"
    elif type(setting) == unreal.MoviePipelineDeferredPass_Unlit:
        return "Deferred Rendering (Unlit)"
    elif type(setting) == unreal.MoviePipelinePanoramicPass:
        return "Panoramic Rendering"
    else:
        return ''


def getFrameTimes(path, firstTime):
    files = os.listdir(path)
    returnList = []
    prevDate = firstTime

    for filename in files:
        file = os.path.join(path, filename)
        if os.path.isfile(file):
            currDate = datetime.fromtimestamp(os.path.getmtime(file))
            delta = currDate - prevDate
            prevDate = currDate
            returnList.append(delta.total_seconds())

    return returnList


def getOutputAndRenderTypes(configs):
    outputTypes = []
    renderTypes = []
    for setting in configs:
        output = checkOutputType(setting)
        render = checkRenderType(setting)
        if output != '':
            outputTypes.append(output)
        if render != '':
            renderTypes.append(render)

    return outputTypes, renderTypes


def getProjectName(path):
    if not path:
        return ''

    splitPath = path.split("\\")
    if len(splitPath) == 0:
        return ''

    splitFile = splitPath[-1].split(".")
    if len(splitFile) == 0:
        return ''

    return splitFile[0]


def getRenderSettings(masterConfig):
    outputTypes, renderTypes = getOutputAndRenderTypes(masterConfig.get_all_settings())
    outputSettings = OutputSettings.from_unreal(masterConfig.find_setting_by_class(unreal.MoviePipelineOutputSetting))

    returnVal = RenderSettings(output_types=outputTypes, render_types=renderTypes, output_settings=outputSettings)

    aaConfig = masterConfig.find_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
    consoleConfig = masterConfig.find_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
    highResConfig = masterConfig.find_setting_by_class(unreal.MoviePipelineHighResSetting)

    if aaConfig:
        returnVal.aa_settings = AASettings.from_unreal(aaConfig)
    if consoleConfig:
        returnVal.console_settings = ConsoleSettings.from_unreal(consoleConfig)
    if highResConfig:
        returnVal.high_res_settings = HighResSettings.from_unreal(highResConfig)

    return returnVal


def get_size(memoryBytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if memoryBytes < factor:
            return f"{memoryBytes:.2f}{unit}{suffix}"
        memoryBytes /= factor


def process_settings(u_preset, passedConfig, passedOverrides):
    dictionaryPassedConfig = eval(unreal.TextLibrary.conv_text_to_string(passedConfig))
    dictionaryPassedOverrides = eval(unreal.TextLibrary.conv_text_to_string(passedOverrides))

    OutputSettingsOverride.changeUnreal(dictionaryPassedConfig["output_settings"],
                                        dictionaryPassedOverrides["output_settings_flags"], u_preset)
    AASettingsOverride.changeUnreal(dictionaryPassedConfig["aa_settings"],
                                    dictionaryPassedOverrides["aa_settings_flags"], u_preset)
    ConsoleSettingsOverride.changeUnreal(dictionaryPassedConfig["console_settings"],
                                         dictionaryPassedOverrides["console_settings_flags"], u_preset)
    HighResSettingsOverride.changeUnreal(dictionaryPassedConfig["high_res_settings"],
                                         dictionaryPassedOverrides["high_res_settings_flags"], u_preset)

    return u_preset
