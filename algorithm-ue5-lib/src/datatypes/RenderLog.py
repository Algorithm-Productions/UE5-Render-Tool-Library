from datetime import datetime

from .enums import LogType
from .abstracts.StorableEntity import StorableEntity


class RenderLog(StorableEntity):
    DATABASE = './database/logs'

    def __init__(
            self,
            cleared=False,
            jobUUID='',
            log='',
            logType=None,
            message='',
            timestamp=None,
            uuid=''
    ):
        super().__init__(uuid)
        self.cleared = cleared
        self.jobUUID = jobUUID
        self.log = log
        self.logType = logType or LogType.INFO
        self.message = message
        self.timestamp = timestamp or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @classmethod
    def from_dict(cls, data):
        cleared = data["cleared"] if (data and data["cleared"]) else False
        jobUUID = data["jobUUID"] if (data and data["jobUUID"]) else ''
        log = data["log"] if (data and data["log"]) else ''
        logType = data["logType"].upper() if \
            (data and data["logType"] and LogType.contains(data["logType"].upper())) else LogType.INFO
        message = data["message"] if (data and data["message"]) else ''
        timestamp = data['timestamp'] if (data and data['timestamp']) else ''
        uuid = data["uuid"] if (data and data["uuid"]) else ''

        return cls(
            cleared=cleared,
            jobUUID=jobUUID,
            log=log,
            logType=logType,
            message=message,
            timestamp=timestamp,
            uuid=uuid
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
