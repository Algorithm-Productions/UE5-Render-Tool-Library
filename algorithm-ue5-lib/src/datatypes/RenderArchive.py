from .abstracts.StorableEntity import StorableEntity
from ..datatypes.HardwareStats import HardwareStats
from ..datatypes.RenderRequest import RenderRequest
from ..datatypes.RenderSettings import RenderSettings


class RenderArchive(StorableEntity):
    DATABASE = './database/archive'

    def __init__(
            self,
            avg_frame=0,
            finish_time='',
            frame_map=None,
            hardware_stats=None,
            project_name='',
            render_request=None,
            render_settings=None,
            total_time='',
            uuid=''
    ):
        super().__init__((uuid or render_request.uuid))
        self.avg_frame = avg_frame
        self.finish_time = finish_time
        self.frame_map = [] if frame_map is None else frame_map
        self.hardware_stats = hardware_stats
        self.project_name = project_name
        self.render_request = render_request
        self.render_settings = render_settings
        self.total_time = total_time

    @classmethod
    def from_dict(cls, data):
        avg_frame = data["avg_frame"] if (data and data["avg_frame"]) else 0
        finish_time = data["finish_time"] if (data and data["finish_time"]) else ''
        frame_map = data["frame_map"] if (data and data["frame_map"]) else []
        hardware_stats = HardwareStats.from_dict(data["hardware_stats"]) if (data and data["hardware_stats"]) else {}
        project_name = data["project_name"] if (data and data["project_name"]) else ''
        render_request = RenderRequest.from_dict(data["render_request"]) if (data and data["render_request"]) else {}
        render_settings = RenderSettings.from_dict(data["render_settings"]) if \
            (data and data["render_settings"]) else {}
        total_time = data["total_time"] if (data and data["total_time"]) else ''
        uuid = data["uuid"] if (data and data["uuid"]) else ''

        return cls(
            avg_frame=avg_frame,
            finish_time=finish_time,
            frame_map=frame_map,
            hardware_stats=hardware_stats,
            project_name=project_name,
            render_request=render_request,
            render_settings=render_settings,
            total_time=total_time,
            uuid=uuid
        )

    def copy(self):
        return RenderArchive(
            avg_frame=self.avg_frame,
            finish_time=self.finish_time,
            frame_map=self.frame_map,
            hardware_stats=self.hardware_stats,
            project_name=self.project_name,
            render_request=self.render_request,
            render_settings=self.render_settings,
            total_time=self.total_time,
            uuid=self.uuid
        )

    def to_dict(self):
        copy = self.copy()
        if self.hardware_stats:
            copy.hardware_stats = self.hardware_stats.to_dict()
        if self.render_request:
            copy.render_request = self.render_request.to_dict()
        if self.render_settings:
            copy.render_settings = self.render_settings.to_dict()
        return copy.__dict__
