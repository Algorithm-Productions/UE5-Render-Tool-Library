from datetime import datetime
import GPUtil
import platform
import psutil
import statistics
import time
import unreal

from .CustomUnrealPreset import CustomUnrealPreset
from .datatypes import HardwareStats
from .datatypes.enums import LogType, RenderStatus
from .utils.UnrealUtils import getFrameTimes, getProjectName, getRenderSettings, get_size, process_settings


@unreal.uclass()
class RenderExecutor(unreal.MoviePipelinePythonHostExecutor):
    config_path = unreal.uproperty(unreal.Text)
    finalJobConfig = unreal.uproperty(unreal.MoviePipelineMasterConfig)
    firstFrameTime = unreal.uproperty(unreal.Text)
    job_id = unreal.uproperty(unreal.Text)
    level_path = unreal.uproperty(unreal.Text)
    passedConfig = unreal.uproperty(unreal.Text)
    passedOverrides = unreal.uproperty(unreal.Text)
    pipeline = unreal.uproperty(unreal.MoviePipeline)
    project_name = unreal.uproperty(unreal.Text)
    queue = unreal.uproperty(unreal.MoviePipelineQueue)
    sequence_path = unreal.uproperty(unreal.Text)
    server_api_url = unreal.uproperty(unreal.Text)

    def _post_init(self):
        self.config_path = ""
        self.finalJobConfig = None
        self.firstFrameTime = ""
        self.http_response_recieved_delegate.add_function_unique(self, "on_http_response_received")
        self.job_id = ""
        self.level_path = ""
        self.passedConfig = ""
        self.passedOverrides = ""
        self.pipeline = None
        self.project_name = ""
        self.queue = None
        self.sequence_path = ""
        self.server_api_url = "http://127.0.0.1:5000/api"

    def parse_argument(self):
        (cmd_tokens, cmd_switches, cmd_parameters) = unreal.SystemLibrary.parse_command_line(
            unreal.SystemLibrary.get_command_line())

        self.level_path = cmd_tokens[0]

        self.config_path = cmd_parameters['MoviePipelineConfig']
        self.job_id = cmd_parameters['JobId']
        self.passedConfig = cmd_parameters['RenderSettings']
        self.passedOverrides = cmd_parameters['ConfigOverride']
        self.project_name = getProjectName(cmd_parameters["ProjectPath"])
        self.sequence_path = cmd_parameters['LevelSequence']

    def add_job(self):
        self.send_http_request(
            "{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url)),
            "POST",
            '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                    "Job {} Began Rendering!".format(self.job_id),
                                    "Job {} Began Rendering!".format(self.job_id), LogType.INFO),
            {"Content-Type": "application/json"}
        )

        job = self.queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.map = unreal.SoftObjectPath(unreal.TextLibrary.conv_text_to_string(self.level_path))
        job.sequence = unreal.SoftObjectPath(unreal.TextLibrary.conv_text_to_string(self.sequence_path))

        preset_path = unreal.SoftObjectPath(unreal.TextLibrary.conv_text_to_string(self.config_path))
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

        progress = 100 * unreal.MoviePipelineLibrary.get_completion_percentage(self.pipeline)
        status = RenderStatus.RENDERING
        time_estimate = unreal.MoviePipelineLibrary.get_estimated_time_remaining(self.pipeline)

        if not time_estimate:
            time_estimate = unreal.Timespan.MAX_VALUE

        days, hours, minutes, seconds, _ = time_estimate.to_tuple()
        time_estimate = '{}h:{}m:{}s'.format(hours, minutes, seconds)

        if self.firstFrameTime == "":
            self.firstFrameTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.send_http_request(
            "{}/put/{}".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url), self.job_id),
            "PUT",
            '{};{};{}'.format(progress, time_estimate, status),
            unreal.Map(str, str)
        )

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
            self.send_http_request(
                "{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url)),
                "POST",
                '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                        "Job {} Errored!".format(self.job_id), "...", LogType.ERROR),
                {"Content-Type": "application/json"}
            )
        else:
            self.send_http_request(
                "{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url)),
                "POST",
                '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                        "Job {} Finished Rendering!".format(self.job_id),
                                        "Job {} Finished Rendering!".format(self.job_id),
                                        LogType.INFO), {"Content-Type": "application/json"}
            )

        progress = 100
        time_estimate = 'N/A'
        status = RenderStatus.FINISHED
        self.send_http_request(
            "{}/put/{}".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url), self.job_id),
            "PUT",
            '{};{};{}'.format(progress, time_estimate, status),
            unreal.Map(str, str)
        )

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

        self.send_http_request(
            "{}/archives/post".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url)),
            "POST",
            '{};{};{};{};{};{};{}'.format(self.job_id, self.project_name, hardwareStats, finishTime,
                                          avgFrame, frameTimesArray, renderSettings),
            {"Content-Type": "application/json"}
        )

    @unreal.ufunction(ret=None,
                      params=[unreal.MoviePipelinePythonHostExecutor, unreal.MoviePipeline, bool, unreal.Text])
    def error_implementation(self, executor, pipeline, fatal, error_reason):
        self.send_http_request(
            "{}/logs/post".format(unreal.TextLibrary.conv_text_to_string(self.server_api_url)),
            "POST",
            '{};{};{};{};{}'.format(self.job_id, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                    "Job {} Errored!".format(self.job_id),
                                    "...", LogType.ERROR),
            {"Content-Type": "application/json"}
        )

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
