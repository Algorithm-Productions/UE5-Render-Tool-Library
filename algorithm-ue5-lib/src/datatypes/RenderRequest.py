from datetime import datetime, timedelta
import platform

from .abstracts.StorableEntity import StorableEntity
from .enums import RenderStatus
from .RenderSettings import RenderSettings
from .RenderSettingsOverride import RenderSettingsOverride


class RenderRequest(StorableEntity):
    DATABASE = './database'

    def __init__(
            self,
            category='',
            config_override=None,
            config_path='',
            estimated_finish='',
            level_path='',
            name='',
            owner='',
            priority=0,
            progress=0,
            project_path='',
            render_settings=None,
            sequence_path='',
            status='',
            tags=None,
            time_created='',
            time_estimate='',
            uuid='',
            worker=''
    ):
        super().__init__(uuid)
        self.category = category
        self.config_override = config_override
        self.config_path = config_path
        self.estimated_finish = estimated_finish
        self.level_path = level_path
        self.name = name
        self.owner = owner or platform.node()
        self.priority = priority
        self.progress = progress
        self.project_path = project_path
        self.render_settings = render_settings
        self.sequence_path = sequence_path
        self.status = status or RenderStatus.ABANDONED
        self.tags = [] if tags is None else tags
        self.time_created = time_created or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.time_estimate = time_estimate
        self.worker = worker

        self.calcFinish(estimated_finish)

    @classmethod
    def from_dict(cls, data):
        category = data["category"] if (data and data["category"]) else ''
        config_override = RenderSettingsOverride.from_dict(data["config_override"]) if \
            (data and data["config_override"]) else None
        config_path = data["config_path"] if (data and data["config_path"]) else ''
        estimated_finish = data["estimated_finish"] if (data and data["estimated_finish"]) else ''
        level_path = data["level_path"] if (data and data["level_path"]) else ''
        name = data["name"] if (data and data["name"]) else ''
        owner = data["owner"] if (data and data["owner"]) else ''
        priority = data["priority"] if (data and data["priority"]) else 0
        progress = data["progress"] if (data and data["progress"]) else 0
        project_path = data["project_path"] if (data and data["project_path"]) else ''
        render_settings = RenderSettings.from_dict(data["render_settings"]) if \
            (data and data["render_settings"]) else None
        status = data["status"] if (data and data["status"]) else RenderStatus.ABANDONED
        sequence_path = data["sequence_path"] if (data and data["sequence_path"]) else ''
        tags = data["tags"] if (data and data["tags"]) else []
        time_created = data["time_created"] if (data and data["time_created"]) else ''
        time_estimate = data["time_estimate"] if (data and data["time_estimate"]) else ''
        uuid = data["uuid"] if (data and data["uuid"]) else ''
        worker = data["worker"] if (data and data["worker"]) else ''

        return cls(
            category=category,
            config_override=config_override,
            config_path=config_path,
            estimated_finish=estimated_finish,
            level_path=level_path,
            name=name,
            owner=owner,
            priority=priority,
            progress=progress,
            project_path=project_path,
            render_settings=render_settings,
            status=status,
            sequence_path=sequence_path,
            tags=tags,
            time_created=time_created,
            time_estimate=time_estimate,
            uuid=uuid,
            worker=worker
        )

    def assign(self, worker):
        self.update({"worker": worker})

    def calcFinish(self, defaultVal=''):
        value = defaultVal
        if self.time_estimate == 'N/A':
            value = 'N/A'
        elif self.time_estimate != '':
            start = datetime.now()
            end = datetime.strptime(self.time_estimate, '%Hh:%Mm:%Ss')
            delta = timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
            value = defaultVal or (start + delta).strftime("%m/%d/%Y, %H:%M:%S")

        self.estimated_finish = value

    def copy(self):
        return RenderRequest(
            category=self.category,
            config_override=self.config_override,
            config_path=self.config_path,
            estimated_finish=self.estimated_finish,
            level_path=self.level_path,
            name=self.name,
            owner=self.owner,
            priority=self.priority,
            progress=self.progress,
            project_path=self.project_path,
            render_settings=self.render_settings,
            status=self.status,
            sequence_path=self.sequence_path,
            tags=self.tags,
            time_created=self.time_created,
            time_estimate=self.time_estimate,
            uuid=self.uuid,
            worker=self.worker
        )

    def to_dict(self):
        copy = self.copy()
        if self.config_override:
            copy.config_override = self.config_override.to_dict()
        if self.render_settings:
            copy.render_settings = self.render_settings.to_dict()
        return copy.__dict__
