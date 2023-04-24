import os
import platform
import uuid as genUUID

from datetime import datetime
from flask import Flask

from .utils.ManagerUtils import buildLog
from .datatypes import RenderLog, RenderArchive, RenderRequest


MANAGER_NAME = platform.node()


class ManagerFlaskApp(Flask):
    WORKERS = []

    def add_worker(self, worker):
        if worker not in self.WORKERS:
            self.WORKERS.append(worker)
            return "Added Worker"
        else:
            return "Worker Already Active"

    def remove_worker(self, worker):
        if worker in self.WORKERS:
            self.WORKERS.remove(worker)
            return "Removed Worker"
        else:
            return "Worker Not Active"

    def run(self, host, port, database_path, debug=False, load_dotenv=True, **options):
        self.check_database(database_path)

        if not debug:
            self.emit_start_log()
        try:
            super().run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
        finally:
            if not debug:
                self.emit_shutdown_log()

    def check_database(self, database_path):
        with self.app_context():
            os.makedirs(database_path, exist_ok=True)
            os.makedirs(os.path.join(database_path, 'archive'), exist_ok=True)
            os.makedirs(os.path.join(database_path, 'logs'), exist_ok=True)

    def emit_start_log(self):
        with self.app_context():
            RenderLog(uuid=str(genUUID.uuid4())[:5],
                      jobUUID='',
                      timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      message='App Manager at {} is Starting!'.format(MANAGER_NAME),
                      log='App Manager at {} is Starting!'.format(MANAGER_NAME),
                      logType="INFO").save_self()

    def emit_shutdown_log(self):
        with self.app_context():
            RenderLog(uuid=str(genUUID.uuid4())[:5],
                      jobUUID='',
                      timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      message='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                      log='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                      logType="CRITICAL").save_self()


def abstract_read_one(entity):
    return entity.to_dict() if entity and entity.to_dict() else {}


def abstract_read_all(entities):
    if not entities:
        return {"results": []}

    jsons = [entity.to_dict() if entity and entity.to_dict() else {} for entity in entities]

    return {"results": jsons}


def abstract_update(entity, content):
    if (not entity) or (not content) or (not eval(content)):
        return {}

    parsedContent = eval(content)
    entity.update(parsedContent)
    return entity.to_dict()


def abstract_delete_all(entityType, shouldLog):
    res = None
    if entityType == "Requests":
        res = RenderRequest.read_all()
        RenderRequest.remove_all()
    elif entityType == "Archives":
        res = RenderArchive.read_all()
        RenderArchive.remove_all()
    elif entityType == "Logs":
        res = RenderLog.read_all()
        RenderLog.remove_all()

    if not res:
        return {"results": {}}
    if shouldLog:
        buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      'Deleting All {} from DB'.format(entityType),
                      'Deleting All {} from DB'.format(entityType), "CRITICAL"]).save_self()

    return {"results": [r.to_dict() if r else {} for r in res]}


def abstract_delete(uuid, entityType, shouldLog):
    res = None
    if entityType == "Request":
        res = RenderRequest.read(uuid)
    elif entityType == "Archive":
        res = RenderArchive.read(uuid)
    elif entityType == "Log":
        res = RenderLog.read(uuid)

    if not res:
        return {}
    if shouldLog:
        buildLog(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        'Deleting {} {} from DB'.format(entityType, uuid),
                        'Deleting {} {} from DB'.format(entityType, uuid), "WARN"]).save_self()

    res.remove_self()
    return res.to_dict()
