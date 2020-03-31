import DBPackage.DBService as api
import datetime


def RFIDHandler(clientId, cardId):
    if api.doesCardExist(cardId):
        worker = api.getCardWorker(cardId)
        if worker == None:
            api.addUnknownUsage(cardId)
            return None
        elif api.isWorkerLoggedIn(worker['Worker']):
            api.addLogInOut(clientId, worker['Worker'], 'o')
            api.logOutWorker(worker['Worker'])
            return worker
        else:
            api.addLogInOut(clientId, worker['Worker'], 'i')
            api.logInWorker(worker['Worker'])
            return worker
    else:
        api.addCard(cardId, None)
        api.addUnknownUsage(cardId)
        return None


def getDataBaseState():
    return [api.getClientsList(),
            api.getWorkersList(),
            api.getCardsList(),
            api.getLogsInOutList(),
            api.getUnknownUsagesList()]


def newWorker(firstName, lastName):
    api.addWorker(firstName, lastName)
    return api.getWorkersList()


def unsetCard(cardId):
    if api.doesCardExist(cardId):
        api.setCard(cardId, None)
    else:
        api.addCard(cardId, None)


def setCard(cardId, workerId):
    if api.doesCardExist(cardId):
        api.setCard(cardId, workerId)
    else:
        api.addCard(cardId, workerId)


def getWorkersList():
    return api.getWorkersList()


def generateRaport(workerId):
    loggs = api.getWorkersInOut(workerId)
    worker = api.getWorkerData(workerId)
    path = "%s_%s_%d_%s.csv" % (
        worker['firstName'], worker['LastName'], worker['IdW'], datetime.datetime.now().date())
    inList = []
    outList = []
    for log in loggs:
        if log['InOut'] == 'i':
            inList.append(log['DateL'])
        else:
            outList.append(log['DateL'])

    if len(inList) > len(outList):
        outList.append(str(datetime.datetime.now()))

    workTime = datetime.timedelta()

    file = open(path, 'w')

    file.write("In;Out;Time in work\n")

    for i in range(0, len(inList)):
        logIn = datetime.datetime.strptime(inList[i], "%Y-%m-%d %H:%M:%S.%f")
        logOut = datetime.datetime.strptime(outList[i], "%Y-%m-%d %H:%M:%S.%f")
        oneTimeWork = logOut - logIn
        workTime += oneTimeWork
        floatOneTime = (oneTimeWork.total_seconds() / 3600)
        file.write("%s;%s;%f\n" %
                   (inList[i], outList[i], floatOneTime))
    floatTime = (workTime.total_seconds() / 3600)
    file.write(";All time in work;%f" % floatTime)

    file.close()

def closeDB():
    api.db.cur.close()