import logging
import os
import subprocess
import threading
import time

from .datatypes.enums import RenderStatus

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Worker(threading.Thread):
    def __init__(self, client, name, unrealPath):
        threading.Thread.__init__(self)
        self.client = client
        self.name = name
        self.running = True
        self.unrealPath = unrealPath

    def render(self, render_request):
        command = [
            self.unrealPath,
            render_request.project_path,
            render_request.level_path,

            "-ConfigOverride={}".format(render_request.config_override),
            "-JobId={}".format(render_request.uuid),
            "-LevelSequence={}".format(render_request.sequence_path),
            "-MoviePipelineConfig={}".format(render_request.config_path),
            "-ProjectPath={}".format(render_request.project_path),
            "-RenderSettings={}".format(render_request.render_settings),

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
                    req
                )

                LOGGER.info("finished rendering job %s", uuid)

            time.sleep(10)
            LOGGER.info('current job(s) finished, searching for new job(s)')

    def stop(self):
        self.running = False
        self.client.delete_worker(self.name)
