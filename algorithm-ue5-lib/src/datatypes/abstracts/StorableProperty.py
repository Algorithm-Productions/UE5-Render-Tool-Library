from abc import ABC, abstractmethod


class StorableProperty(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

    def to_dict(self):
        return self.__dict__
