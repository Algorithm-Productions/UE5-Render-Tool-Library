import logging
import os
import subprocess
import threading
import time

from .datatypes.enums import RenderStatus


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Worker(threading.Thread):
    def __init__(self, name, client, unrealPath):
        threading.Thread.__init__(self)
        self.name = name
        self.client = client
        self.unrealPath = unrealPath
        self.running = True

    def run(self):
        LOGGER.info('Starting render worker %s', self.name)
        self.client.add_worker(self.name)
        while self.running:
            reqs = self.client.get_all_requests()
            uuids = [req.uuid for req in reqs
                     if req.worker == self.name and
                     req.status == RenderStatus.READY]

            for uuid in uuids:
                LOGGER.info('rendering job %s', uuid)

                req = self.client.get_request(uuid)
                output = self.render(
                    uuid,
                    req.project_path,
                    req.level_path,
                    req.sequence_path,
                    req.config_path,
                    req.config_override.to_dict(),
                    req.render_settings.to_dict()
                )

                LOGGER.info("finished rendering job %s", uuid)

            time.sleep(10)
            LOGGER.info('current job(s) finished, searching for new job(s)')

    def stop(self):
        self.running = False
        self.client.delete_worker(self.name)

    def render(self, uuid, project_path, level_path, sequence_path, config_path, config_override, render_settings):
        command = [
            self.unrealPath,
            project_path,

            level_path,
            "-JobId={}".format(uuid),
            "-ProjectPath={}".format(project_path),
            "-LevelSequence={}".format(sequence_path),
            "-MoviePipelineConfig={}".format(config_path),
            "-ConfigOverride={}".format(config_override),
            "-RenderSettings={}".format(render_settings),

            "-game",
            "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor",
            "-ExecutorPythonClass=/Engine/PythonTypes.RenderExecutor",

            "-windowed",
            "-resX=1280",
            "-resY=720",

            "-StdOut",
            "-FullStdOutLogOutput"
        ]
        env = os.environ.copy()
        env["UE_PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        return proc.communicate()
