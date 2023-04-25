from datetime import datetime
import time
import uuid as genUUID

from ..datatypes import HardwareStats, RenderArchive, RenderLog, RenderRequest, RenderSettings
from ..datatypes.enums import LogType, RenderStatus


def abstract_read(entity):
    return entity.to_dict() if entity and entity.to_dict() else {}


def abstract_read_all(entities):
    if not entities:
        return {"results": []}

    jsons = [entity.to_dict() if entity and entity.to_dict() else {} for entity in entities]
    return {"results": jsons}


def abstract_delete_all(entityType, shouldLog):
    res = None
    if entityType == "Archives":
        res = RenderArchive.read_all()
        RenderArchive.remove_all()
    elif entityType == "Logs":
        res = RenderLog.read_all()
        RenderLog.remove_all()
    elif entityType == "Requests":
        res = RenderRequest.read_all()
        RenderRequest.remove_all()

    if not res:
        return {"results": {}}
    if shouldLog:
        buildLog('', ['Deleting All {} from DB'.format(entityType), "WARN",
                      'Deleting All {} from DB'.format(entityType),
                      datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), '']).save_self()

    return {"results": [r.to_dict() if r else {} for r in res]}


def abstract_delete(entityType, shouldLog, uuid):
    res = None
    if entityType == "Archive":
        res = RenderArchive.read(uuid)
    elif entityType == "Log":
        res = RenderLog.read(uuid)
    elif entityType == "Request":
        res = RenderRequest.read(uuid)

    if not res:
        return {}
    if shouldLog:
        buildLog(uuid, ['Deleting {} {} from DB'.format(entityType, uuid), "WARN",
                        'Deleting {} {} from DB'.format(entityType, uuid),
                        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), uuid]).save_self()

    res.remove_self()
    return res.to_dict()


def abstract_update(content, entity):
    if (not content) or (not eval(content)) or (not entity):
        return {}

    parsedContent = eval(content)
    entity.update(parsedContent)
    return entity.to_dict()


def assign_request(req, worker):
    req.assign(worker)
    req.update({"status": RenderStatus.READY})


def buildArchive(metadata, uuid, renderRequest):
    renderArchive = RenderArchive(uuid=uuid, render_request=renderRequest)
    renderArchive.avg_frame = float(metadata[4])
    renderArchive.hardware_stats = HardwareStats.from_dict(eval(metadata[2]))
    renderArchive.finish_time = metadata[3]
    renderArchive.frame_map = metadata[5].strip('][').split(', ')
    renderArchive.project_name = metadata[1]
    renderArchive.render_settings = RenderSettings.from_dict(eval(metadata[6]))
    renderArchive.total_time = str(
        datetime.strptime(renderArchive.finish_time, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(
            renderRequest.time_created, "%m/%d/%Y, %H:%M:%S"))

    return renderArchive


def buildLog(jobUUID, metadata):
    return RenderLog(jobUUID=jobUUID, log=metadata[1],
                     logType=(metadata[2].upper() if LogType.contains(metadata[4].upper()) else LogType.INFO),
                     message=metadata[3], timestamp=metadata[4], uuid=str(genUUID.uuid4()))


def checkAgeAndClear(log):
    curDate = datetime.now()
    logDate = datetime.strptime(log.timestamp, "%m/%d/%Y, %H:%M:%S")

    diff = curDate - logDate
    if diff.days >= 7:
        log.remove()
        return True
    else:
        return False


def getLogsToDisplay():
    allLogs = RenderLog.read_all()
    objList = []

    for log in allLogs:
        deleted = checkAgeAndClear(log)
        if log.logType != LogType.INFO and (not deleted) and (not log.cleared):
            objList.append(log)

    objList.sort()
    returnList = [log.to_dict() for log in objList]

    return returnList


def new_request_trigger(logger, req, worker):
    if req.worker:
        req.update({"status": RenderStatus.READY})
        return

    assign_request(req, worker)

    time.sleep(3)
    logger.info('assigned job %s to %s', req.uuid, worker)
