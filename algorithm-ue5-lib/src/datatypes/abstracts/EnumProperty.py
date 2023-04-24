from abc import ABC, abstractmethod


class EnumProperty(ABC):
    @classmethod
    @abstractmethod
    def contains(cls, item):
        pass
