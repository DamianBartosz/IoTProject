import datetime
import DBPackage.DBconfig as db


def addClient(nameC):
    db.cur.execute('INSERT INTO Clients VALUES(NULL, ?);', (nameC,))
    db.con.commit()


def addWorker(firstName, lastName):
    db.cur.execute('INSERT INTO Workers VALUES(NULL, ?, ?, ?);',
                   (firstName, lastName, 0))
    db.con.commit()


def addCard(cardId, workerId):
    db.cur.execute('INSERT INTO Cards VALUES(?, ?);', (cardId, workerId))
    db.con.commit()


def addUnknownUsage(cardId):
    db.cur.execute('INSERT INTO UnknownUsages VALUES(NULL, ?, ?);',
                   (cardId, datetime.datetime.now()))
    db.con.commit()


def addLogInOut(clientId, workerId, inOut):
    db.cur.execute('INSERT INTO LogsInOut VALUES(NULL, ?, ?, ?, ?);',
                   (clientId, workerId, inOut, datetime.datetime.now()))
    db.con.commit()


def deleteClient(clientId):
    db.cur.execute('DELETE FROM Clients WHERE IdC=?', (clientId,))
    db.con.commit()


def setCard(cardId, workerId):
    db.cur.execute('UPDATE Cards SET Worker=? WHERE IdCard=?',
                   (workerId, cardId))
    db.con.commit()


def logInWorker(workerId):
    db.cur.execute('UPDATE Workers SET LoggedIn=? WHERE IdW=?', (1, workerId))
    db.con.commit()


def logOutWorker(workerId):
    db.cur.execute('UPDATE Workers SET LoggedIn=? WHERE IdW=?', (0, workerId))
    db.con.commit()


def isWorkerLoggedIn(workerId):
    db.cur.execute('SELECT LoggedIn FROM Workers WHERE IdW=?', (workerId,))
    if db.cur.fetchone()['LoggedIn'] == 1:
        return True
    else:
        return False


def getWorkerData(workerId):
    db.cur.execute(
        'SELECT IdW, FirstName, LastName, LoggedIn FROM Workers WHERE IdW=?', (workerId,))
    return db.cur.fetchone()


def getClientsList():
    db.cur.execute('SELECT IdC, NameC From Clients')
    return db.cur.fetchall()


def getWorkersList():
    db.cur.execute('SELECT IdW, FirstName, LastName, LoggedIn From Workers')
    return db.cur.fetchall()


def getCardsList():
    db.cur.execute(
        'SELECT IdCard, Worker, FirstName, LastName From Cards JOIN Workers ON Worker = IdW ')
    takenCards = db.cur.fetchall()
    db.cur.execute('SELECT IdCard, Worker From Cards WHERE Worker is null')
    return takenCards + db.cur.fetchall()


def getUnknownUsagesList():
    db.cur.execute('SELECT IdU, Card, DateU From UnknownUsages')
    return db.cur.fetchall()


def getLogsInOutList():
    db.cur.execute(
        'SELECT IdL, Client, NameC, Worker, FirstName, LastName, InOut, DateL From LogsInOut JOIN Clients JOIN Workers ON Client = IdC and Worker = IdW')
    return db.cur.fetchall()


def getCardWorker(cardId):
    db.cur.execute(
        'SELECT Cards.Worker, Workers.FirstName, Workers.LastName, Workers.LoggedIn FROM Cards JOIN Workers ON Cards.Worker = Workers.IdW WHERE IdCard=?', (cardId,))
    return db.cur.fetchone()


def doesCardExist(cardId):
    db.cur.execute(
        'SELECT IdCard FROM Cards WHERE IdCard=?', (cardId,))
    if db.cur.fetchone() is None:
        return False
    else:
        return True


def getWorkersInOut(workerId):
    db.cur.execute(
        'SELECT InOut, DateL FROM LogsInOut WHERE Worker=?', (workerId,))
    return db.cur.fetchall()
