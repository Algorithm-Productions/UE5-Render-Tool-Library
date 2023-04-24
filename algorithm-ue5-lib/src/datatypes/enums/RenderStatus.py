from ..abstracts.EnumProperty import EnumProperty


class RenderStatus(EnumProperty):
    ABANDONED = 'ABANDONED'
    CANCELLED = 'CANCELLED'
    ERROR = 'ERROR'
    FINISHED = 'FINISHED'
    READY = 'READY'
    RENDERING = 'RENDERING'
    PAUSED = 'PAUSED'

    @classmethod
    def contains(cls, item):
        return item in [cls.ABANDONED, cls.CANCELLED, cls.ERROR, cls.FINISHED, cls.READY, cls.RENDERING, cls.PAUSED]
