#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import DBPackage.DBService as api
import datetime
import os
from shutil import copy2
import socket
from MQTTConfig import *  # pylint: disable=unused-wildcard-import


def RFIDHandler(clientId, cardId, date):
    if api.doesClientExist(clientId):
        if api.doesCardExist(cardId):
            worker = api.getCardWorker(cardId)
            if worker == None:
                api.addUnknownUsage(clientId, cardId, date)
                return None
            elif api.isWorkerLoggedIn(worker['Worker']):
                api.addLogInOut(clientId, worker['Worker'], 'o', date)
                api.logOutWorker(worker['Worker'])
                return worker
            else:
                api.addLogInOut(clientId, worker['Worker'], 'i', date)
                api.logInWorker(worker['Worker'])
                return worker
        else:
            api.addCard(cardId, None)
            api.addUnknownUsage(clientId, cardId, date)
            return None
    else:
        print("Próba logowania z nieuprawnionego klienta")


def generateReport(workerId):
    loggs = api.getWorkersInOut(workerId)
    worker = api.getWorkerData(workerId)
    path = "Reports/%s_%s_%d_%s.csv" % (
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


def generateTerminalCode(clientName, clientId):
    dirPath = "%s_%d_terminal" % (clientName, clientId)
    dirPath = dirPath.replace(' ', '_')
    os.mkdir(dirPath)
    copy2("Model/RFIDTerminal.py", dirPath)
    copy2("Model/MFRC522.py", dirPath)
    copy2("Model/GPIOconfig.py", dirPath)
    copy2("ca.crt", dirPath)

    config = open("%s/MQTTconfig.py" % dirPath, "w")
    config.write("#!/usr/bin/env python3\n\n")
    config.write("import paho.mqtt.client as mqtt\n\n")
    config.write("terminalID = %d\n" % clientId)
    config.write("broker = '%s'\n" % broker)
    config.write("port = %d\n\n" % port)
    config.write("client = mqtt.Client()\n")
    config.write("client.tls_set('ca.crt')\n")
    config.write(
        "client.username_pw_set(username='client', password='password')\n")
    config.write("client.connect(broker, port)\n")
    config.write("client.loop_start()\n")
    config.close()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(";")
    RFIDHandler(message_decoded[0], message_decoded[1], message_decoded[2])


def subscribe_to_broker():
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/name")


def start():
    connect_to_broker()
    subscribe_to_broker()


def close():
    client.loop_stop()
    client.disconnect()
