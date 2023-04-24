from abc import ABC, abstractmethod


class UnrealDataType(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

    @classmethod
    @abstractmethod
    def from_unreal(cls, unrealClass):
        pass

    def to_dict(self):
        return self.__dict__
