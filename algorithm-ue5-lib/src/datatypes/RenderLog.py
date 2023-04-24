from datetime import datetime

from .enums import LogType
from .abstracts.StorableEntity import StorableEntity


class RenderLog(StorableEntity):
    DATABASE = './database/logs'

    def __init__(
            self,
            cleared=False,
            uuid='',
            jobUUID='',
            timestamp=None,
            message='',
            log='',
            logType=None
    ):
        super().__init__(uuid)
        self.jobUUID = jobUUID or ''
        self.timestamp = timestamp or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.message = message or ''
        self.log = log or ''
        self.logType = logType or LogType.INFO
        self.cleared = cleared

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        jobUUID = data.get('jobUUID') or ''
        timestamp = data.get('timestamp') or ''
        message = data.get('message') or ''
        log = data.get('log') or ''
        logType = (data.get('logType').upper() if (
                    data.get('logType') and LogType.contains(data.get('logType').upper())) else '')
        cleared = data.get('cleared')

        return cls(
            uuid=uuid,
            jobUUID=jobUUID,
            timestamp=timestamp,
            message=message,
            log=log,
            logType=logType,
            cleared=cleared
        )

    def __eq__(self, other):
        return self.logType == other.logType and self.timestamp == other.timestamp

    def __lt__(self, other):
        if self.logType == other.logType:
            return datetime.strptime(self.timestamp, "%m/%d/%Y, %H:%M:%S") > datetime.strptime(other.timestamp,
                                                                                               "%m/%d/%Y, %H:%M:%S")
        else:
            return LogType.getNumVal(self.logType) < LogType.getNumVal(
                other.logType)

    def clear(self):
        self.update({"cleared": True})
