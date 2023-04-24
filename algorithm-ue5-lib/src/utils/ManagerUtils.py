import time
import uuid as genUUID

from datetime import datetime

from ..datatypes import HardwareStats, RenderArchive, RenderLog, RenderSettings
from ..datatypes.enums import LogType, RenderStatus


def new_request_trigger(req, worker, logger):
    if req.worker:
        req.update({"status": RenderStatus.READY})
        return

    assign_request(req, worker)

    time.sleep(3)
    logger.info('assigned job %s to %s', req.uuid, worker)


def assign_request(req, worker):
    req.assign(worker)
    req.update({"status": RenderStatus.READY})


def buildArchive(uuid, renderRequest, metadata):
    renderArchive = RenderArchive(uuid=uuid, render_request=renderRequest)
    renderArchive.project_name = metadata[1]
    renderArchive.hardware_stats = HardwareStats.from_dict(eval(metadata[2]))
    renderArchive.finish_time = metadata[3]
    renderArchive.avg_frame = float(metadata[4])
    renderArchive.frame_map = metadata[5].strip('][').split(', ')
    renderArchive.render_settings = RenderSettings.from_dict(eval(metadata[6]))

    renderArchive.total_time = str(
        datetime.strptime(renderArchive.finish_time, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(
            renderRequest.time_created, "%m/%d/%Y, %H:%M:%S"))

    return renderArchive


def buildLog(jobUUID, metadata):
    return RenderLog(uuid=str(genUUID.uuid4())[:5], jobUUID=jobUUID, timestamp=metadata[1], message=metadata[2],
                     log=metadata[3], logType=(metadata[4].upper() if LogType.contains(metadata[4].upper()) else ''))


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
