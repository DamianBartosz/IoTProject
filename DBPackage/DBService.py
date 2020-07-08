#!/usr/bin/env python3

import datetime
import sqlite3


def addClient(nameC):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO Clients VALUES(NULL, ?);', (nameC,))
    con.commit()
    cur.execute('SELECT * FROM Clients ORDER BY IdC DESC LIMIT 1;')
    newClient = cur.fetchone()
    con.close()
    return newClient


def addWorker(firstName, lastName):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO Workers VALUES(NULL, ?, ?, ?);',
                (firstName, lastName, 0))
    con.commit()
    cur.execute('SELECT * FROM Workers ORDER BY IdW DESC LIMIT 1;')
    newWorker = cur.fetchone()
    con.close()
    return newWorker


def addCard(cardId, workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO Cards VALUES(?, ?);', (cardId, workerId))
    con.commit()
    con.close()


def addUnknownUsage(clientId, cardId, date):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO UnknownUsages VALUES(NULL, ?, ?, ?);',
                (clientId, cardId, date))
    con.commit()
    con.close()


def addLogInOut(clientId, workerId, inOut, date):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO LogsInOut VALUES(NULL, ?, ?, ?, ?);',
                (clientId, workerId, inOut, date))
    con.commit()
    con.close()


def deleteClient(clientId):
    if(clientId != 1):
        con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('UPDATE LogsInOut SET Client=1 WHERE Client=?', (clientId,))
    cur.execute('UPDATE UnknownUsages SET Client=1 WHERE Client=?', (clientId,))
    cur.execute('DELETE FROM Clients WHERE IdC=?', (clientId,))
    con.commit()
    con.close()


def setCard(cardId, workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('UPDATE Cards SET Worker=? WHERE IdCard=?',
                (workerId, cardId))
    con.commit()
    con.close()


def logInWorker(workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('UPDATE Workers SET LoggedIn=? WHERE IdW=?', (1, workerId))
    con.commit()
    con.close()


def logOutWorker(workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('UPDATE Workers SET LoggedIn=? WHERE IdW=?', (0, workerId))
    con.commit()
    con.close()


def isWorkerLoggedIn(workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT LoggedIn FROM Workers WHERE IdW=?', (workerId,))
    loggedIn = cur.fetchone()['LoggedIn'] == 1
    con.close()
    if loggedIn:
        return True
    else:
        return False


def getWorkerData(workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT IdW, FirstName, LastName, LoggedIn FROM Workers WHERE IdW=?', (workerId,))
    worker = cur.fetchone()
    con.close()
    return worker


def getClientsList():
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT IdC, NameC FROM Clients WHERE IdC>1')
    clientsList = cur.fetchall()
    con.close()
    return clientsList


def getWorkersList():
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT IdW, FirstName, LastName, LoggedIn From Workers')
    workersList = cur.fetchall()
    con.close()
    return workersList


def getCardsList():
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT IdCard, Worker, FirstName, LastName From Cards JOIN Workers ON Worker = IdW ')
    takenCards = cur.fetchall()
    cur.execute('SELECT IdCard, Worker From Cards WHERE Worker is null')
    cardsList = takenCards + cur.fetchall()
    con.close()
    return cardsList


def getUnknownUsagesList():
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT IdU, Client, NameC, Card, DateU From UnknownUsages JOIN Clients ON Client = IdC')
    uuList = cur.fetchall()
    con.close()
    return uuList


def getLogsInOutList():
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT IdL, Client, NameC, Worker, FirstName, LastName, InOut, DateL From LogsInOut JOIN Clients JOIN Workers ON Client = IdC and Worker = IdW')
    lioList = cur.fetchall()
    con.close()
    return lioList


def getCardWorker(cardId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT Worker, FirstName, LastName, LoggedIn FROM Cards JOIN Workers ON Cards.Worker = Workers.IdW WHERE IdCard=?', (cardId,))
    cardWorker = cur.fetchone()
    con.close()
    return cardWorker


def doesCardExist(cardId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT IdCard FROM Cards WHERE IdCard=?', (cardId,))
    cardExist = cur.fetchone() is None
    con.close()
    if cardExist:
        return False
    else:
        return True


def doesClientExist(clientId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT IdC FROM Clients WHERE IdC=?', (clientId,))
    clientExist = cur.fetchone() is None
    con.close()
    if clientExist:
        return False
    else:
        return True


def getWorkersInOut(workerId):
    con = sqlite3.connect('SystemDB.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'SELECT InOut, DateL FROM LogsInOut WHERE Worker=?', (workerId,))
    workersInOut = cur.fetchall()
    con.close()
    return workersInOut
