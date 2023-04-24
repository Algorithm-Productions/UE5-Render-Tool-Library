import socket

from datetime import datetime, timedelta

from .abstracts.StorableEntity import StorableEntity
from .enums import RenderStatus
from .RenderSettings import RenderSettings
from .RenderSettingsOverride import RenderSettingsOverride


class RenderRequest(StorableEntity):
    DATABASE = './database'

    def __init__(
            self,
            uuid='',
            name='',
            owner='',
            worker='',
            time_created='',
            priority=0,
            category='',
            tags=None,
            status='',
            project_path='',
            level_path='',
            sequence_path='',
            config_path='',
            time_estimate='',
            estimated_finish='',
            progress=0,
            config_override=None,
            render_settings=None
    ):
        super().__init__(uuid)
        self.name = name
        self.owner = owner or socket.gethostname()
        self.worker = worker
        self.time_created = time_created or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.priority = priority or 0
        self.category = category
        self.tags = [] if tags is None else tags
        self.status = status or RenderStatus.ABANDONED
        self.project_path = project_path
        self.level_path = level_path
        self.sequence_path = sequence_path
        self.config_path = config_path
        self.time_estimate = time_estimate
        self.progress = progress
        self.estimated_finish = estimated_finish or ''
        self.config_override = config_override
        self.render_settings = render_settings

        self.calcFinish(estimated_finish)

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        name = data.get('name') or ''
        owner = data.get('owner') or ''
        worker = data.get('worker') or ''
        time_created = data.get('time_created') or ''
        priority = data.get('priority') or 0
        category = data.get('category') or ''
        tags = data.get('tags') or []
        status = data.get('status') or ''
        project_path = data.get('project_path')
        level_path = data.get('level_path') or ''
        sequence_path = data.get('sequence_path') or ''
        config_path = data.get('config_path') or ''
        time_estimate = data.get('time_estimate') or ''
        estimated_finish = data.get('estimated_finish') or ''
        progress = data.get('progress') or 0
        config_override = RenderSettingsOverride.from_dict(data.get('config_override')) if data.get(
            'config_override') else None
        render_settings = RenderSettings.from_dict(data.get('render_settings')) if data.get('render_settings') else None

        return cls(
            uuid=uuid,
            name=name,
            owner=owner,
            worker=worker,
            time_created=time_created,
            priority=priority,
            category=category,
            tags=tags,
            status=status,
            project_path=project_path,
            level_path=level_path,
            sequence_path=sequence_path,
            config_path=config_path,
            time_estimate=time_estimate,
            estimated_finish=estimated_finish,
            progress=progress,
            config_override=config_override,
            render_settings=render_settings
        )

    def copy(self):
        return RenderRequest(
            uuid=self.uuid,
            name=self.name,
            owner=self.owner,
            worker=self.worker,
            time_created=self.time_created,
            priority=self.priority,
            category=self.category,
            tags=self.tags,
            status=self.status,
            project_path=self.project_path,
            level_path=self.level_path,
            sequence_path=self.sequence_path,
            config_path=self.config_path,
            time_estimate=self.time_estimate,
            estimated_finish=self.estimated_finish,
            progress=self.progress,
            config_override=self.config_override,
            render_settings=self.render_settings
        )

    def to_dict(self):
        copy = self.copy()
        if self.config_override:
            copy.config_override = self.config_override.to_dict()
        if self.render_settings:
            copy.render_settings = self.render_settings.to_dict()
        return copy.__dict__

    def assign(self, worker):
        self.update({"worker": worker})

    def calcFinish(self, defaultVal, ignoreDefault=False):
        value = ((not ignoreDefault) and defaultVal) or ''
        if self.time_estimate == 'N/A':
            value = 'N/A'
        elif self.time_estimate != '':
            start = datetime.now()
            end = datetime.strptime(self.time_estimate, '%Hh:%Mm:%Ss')
            delta = timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
            value = ((not ignoreDefault) and defaultVal) or (
                (start + delta).strftime("%m/%d/%Y, %H:%M:%S"))

        self.estimated_finish = value
