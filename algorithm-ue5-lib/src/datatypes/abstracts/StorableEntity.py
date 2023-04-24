from abc import ABC, abstractmethod
import json
import logging
import os
import uuid as genUUID

LOGGER = logging.getLogger(__name__)


class StorableEntity(ABC):
    DATABASE = './database'

    def __init__(self, uuid):
        self.uuid = uuid or str(genUUID.uuid4())[:4]

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

    @classmethod
    def read(cls, uuid):
        request_file = os.path.join(cls.DATABASE, '{}.json'.format(uuid))
        with open(request_file, 'r') as fp:
            try:
                request_dict = json.load(fp)
            except Exception as e:
                LOGGER.error('Failed to load request object from db: %s', e)
                return None
        return cls.from_dict(request_dict)

    @classmethod
    def read_all(cls):
        reqs = list()
        files = os.listdir(cls.DATABASE)
        uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
        for uuid in uuids:
            req = cls.read(uuid)
            reqs.append(req)

        return reqs

    @classmethod
    def remove(cls, uuid):
        os.remove(os.path.join(cls.DATABASE, '{}.json'.format(uuid)))

    @classmethod
    def remove_all(cls):
        files = os.path.join(cls.DATABASE, '*.json')
        for file in files:
            os.remove(file)

    @classmethod
    def write_db(cls, data):
        uuid = data['uuid']
        with open(os.path.join(cls.DATABASE, '{}.json'.format(uuid)), 'w') as fp:
            json.dump(data, fp, indent=4)

    def __str__(self):
        return self.to_dict().__str__()

    def remove_self(self):
        self.__class__.remove(self.uuid)

    def save_self(self):
        self.__class__.write_db(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def update(self, data):
        selfDict = self.to_dict()

        for key, item in data.items():
            if key in selfDict.keys():
                selfDict[key] = item

        self.__class__.write_db(selfDict)
