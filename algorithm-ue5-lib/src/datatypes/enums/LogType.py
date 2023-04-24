from ..abstracts.EnumProperty import EnumProperty


class LogType(EnumProperty):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"

    @classmethod
    def contains(cls, item):
        return item in [cls.CRITICAL, cls.ERROR, cls.INFO, cls.WARNING]

    @classmethod
    def getNumVal(cls, logType):
        if logType == LogType.CRITICAL:
            return 4
        elif logType == LogType.ERROR:
            return 3
        elif logType == LogType.INFO:
            return 1
        elif logType == LogType.WARNING:
            return 2
        else:
            return 0
