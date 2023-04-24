import GPUtil
import os
import platform
import psutil
import statistics
import time
import unreal

from datetime import datetime

from .CustomUnrealPreset import CustomUnrealPreset
from .datatypes import HardwareStats, RenderSettings
from .datatypes.enums import LogType, RenderStatus
from .datatypes.overrides import OutputSettingsOverride, HighResSettingsOverride, AASettingsOverride, \
    ConsoleSettingsOverride
from .datatypes.unreal_dt import AASettings, ConsoleSettings, OutputSettings, HighResSettings


@unreal.uclass()
class RenderExecutor(unreal.MoviePipelinePythonHostExecutor):
    pipeline = unreal.uproperty(unreal.MoviePipeline)
    job_id = unreal.uproperty(unreal.Text)
    project_name = unreal.uproperty(unreal.Text)
    finalJobConfig = unreal.uproperty(unreal.MoviePipelineMasterConfig)
    firstFrameTime = unreal.uproperty(unreal.Text)
    passedConfig = unreal.uproperty(unreal.Text)
    passedOverrides = unreal.uproperty(unreal.Text)
    SERVER_API_URL = unreal.uproperty(unreal.Text)

    def _post_init(self):
        self.pipeline = None
        self.queue = None
        self.job_id = ""
        self.project_name = ""
        self.finalJobConfig = None
        self.firstFrameTime = ""
        self.passedConfig = ""
        self.passedOverrides = ""
        self.SERVER_API_URL = "http://127.0.0.1:5000/api"

        self.http_response_recieved_delegate.add_function_unique(self, "on_http_response_received")

    def parse_argument(self):
        (cmd_tokens, cmd_switches, cmd_parameters) = unreal.SystemLibrary.parse_command_line(
            unreal.SystemLibrary.get_command_line())

        self.level_path = cmd_tokens[0]
        self.job_id = cmd_parameters['JobId']
        self.sequence_path = cmd_parameters['LevelSequence']
        self.config_path = cmd_parameters['MoviePipelineConfig']
        self.project_name = getProjectName(cmd_parameters["ProjectPath"])
        self.passedConfig = cmd_parameters['RenderSettings']
        self.passedOverrides = cmd_parameters['ConfigOverride']

    def add_job(self):
        self.send_http_request("{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL)),
                               "POST",
                               '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                       "Job {} Began Rendering!".format(self.job_id),
                                                       "Job {} Began Rendering!".format(self.job_id), LogType.INFO),
                               {"Content-Type": "application/json"})

        job = self.queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.map = unreal.SoftObjectPath(self.level_path)
        job.sequence = unreal.SoftObjectPath(self.sequence_path)

        preset_path = unreal.SoftObjectPath(self.config_path)
        u_preset = unreal.SystemLibrary.conv_soft_obj_path_to_soft_obj_ref(preset_path)
        final_u_preset = CustomUnrealPreset(u_preset)
        process_settings(final_u_preset, self.passedConfig, self.passedOverrides)
        job.set_configuration(final_u_preset)
        self.finalJobConfig = job.get_configuration()

        return job

    @unreal.ufunction(override=True)
    def execute_delayed(self, queue):
        self.parse_argument()

        self.pipeline = unreal.new_object(self.target_pipeline_class, outer=self.get_last_loaded_world(),
                                          base_type=unreal.MoviePipeline)
        self.pipeline.on_movie_pipeline_finished_delegate.add_function_unique(self, "on_job_finished")
        self.pipeline.on_movie_pipeline_work_finished_delegate.add_function_unique(self, "on_pipeline_finished")

        self.queue = unreal.new_object(unreal.MoviePipelineQueue, outer=self)
        job = self.add_job()
        self.pipeline.initialize(job)

    @unreal.ufunction(override=True)
    def on_begin_frame(self):
        super(RenderExecutor, self).on_begin_frame()

        if not self.pipeline:
            return

        status = RenderStatus.RENDERING
        progress = 100 * unreal.MoviePipelineLibrary.get_completion_percentage(self.pipeline)
        time_estimate = unreal.MoviePipelineLibrary.get_estimated_time_remaining(self.pipeline)

        if not time_estimate:
            time_estimate = unreal.Timespan.MAX_VALUE

        days, hours, minutes, seconds, _ = time_estimate.to_tuple()
        time_estimate = '{}h:{}m:{}s'.format(hours, minutes, seconds)

        if self.firstFrameTime == "":
            self.firstFrameTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.send_http_request(
            "{}/put/{}".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL), self.job_id), "PUT",
            '{};{};{}'.format(progress, time_estimate, status), unreal.Map(str, str))

    @unreal.ufunction(ret=None, params=[int, int, str])
    def on_http_response_received(self, index, code, message):
        if code == 200:
            unreal.log(message)
        else:
            unreal.log_error('something wrong with the server!!')

    @unreal.ufunction(override=True)
    def is_rendering(self):
        return False

    @unreal.ufunction(ret=None, params=[unreal.MoviePipeline, bool])
    def on_job_finished(self, pipeline, is_errored):
        self.pipeline = None
        unreal.log("Finished rendering movie!")
        self.on_executor_finished_impl()

        time.sleep(1)

        if is_errored:
            self.send_http_request("{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL)),
                                   "POST",
                                   '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                           "Job {} Errored!".format(self.job_id), "...", LogType.ERROR),
                                   {"Content-Type": "application/json"})
        else:
            self.send_http_request("{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL)),
                                   "POST",
                                   '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                           "Job {} Finished Rendering!".format(self.job_id),
                                                           "Job {} Finished Rendering!".format(self.job_id),
                                                           LogType.INFO), {"Content-Type": "application/json"})

        progress = 100
        time_estimate = 'N/A'
        status = RenderStatus.finished
        self.send_http_request(
            "{}/put/{}".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL), self.job_id), "PUT",
            '{};{};{}'.format(progress, time_estimate, status), unreal.Map(str, str))

        renderSettingsDict = getRenderSettings(self.finalJobConfig).to_dict()

        hardwareStats = HardwareStats(platform.node(), platform.processor(), GPUtil.getGPUs()[0].name,
                                      get_size(psutil.virtual_memory().total),
                                      GPUtil.getGPUs()[0].memoryTotal).to_dict()
        finishTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        renderSettings = str(renderSettingsDict)
        frameTimesArray = getFrameTimes(
            unreal.TextLibrary.conv_text_to_string(renderSettingsDict["output_settings"]["outputDirectory"]),
            datetime.strptime(unreal.TextLibrary.conv_text_to_string(self.firstFrameTime), "%m/%d/%Y, %H:%M:%S"))
        avgFrame = statistics.mean([float(val) for val in frameTimesArray])

        self.send_http_request("{}/archives/post".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL)),
                               "POST",
                               '{};{};{};{};{};{};{}'.format(self.job_id, self.project_name, hardwareStats, finishTime,
                                                             avgFrame, frameTimesArray, renderSettings),
                               {"Content-Type": "application/json"})

    @unreal.ufunction(ret=None,
                      params=[unreal.MoviePipelinePythonHostExecutor, unreal.MoviePipeline, bool, unreal.Text])
    def error_implementation(self, executor, pipeline, fatal, error_reason):
        self.send_http_request("{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.SERVER_API_URL)),
                               "POST",
                               '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                       "Job {} Errored!".format(self.job_id), "...", LogType.ERROR),
                               {"Content-Type": "application/json"})

        return "NO"

    @unreal.ufunction(ret=None, params=[unreal.MoviePipelineOutputData])
    def on_pipeline_finished(self, results):
        output_data = results
        if output_data.success:
            for shot_data in output_data.shot_data:
                render_pass_data = shot_data.render_pass_data
                for k, v in render_pass_data.items():
                    if k.name == 'FinalImage':
                        outputs = v.file_paths


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


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
