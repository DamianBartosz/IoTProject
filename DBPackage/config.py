# -*- coding: utf-8 -*-

import sqlite3

# utworzenie połączenia z bazą
con = sqlite3.connect('SystemDB.db')

# dostęp do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row

# utworzenie obiektu kursora
cur = con.cursor()

# model bazy
cur.execute("""
    CREATE TABLE IF NOT EXISTS Workers (
        IdW INTEGER PRIMARY KEY ASC,
        FirstName varchar(250) NOT NULL,
        LastName varchar(250) NOT NULL,
        LoggedIn BIT NOT NULL
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        IdC INTEGER PRIMARY KEY ASC,
        NameC varchar(250) NOT NULL
    )""")

cur.execute("""
    DROP TABLE IF EXISTS Cards;
    CREATE TABLE IF NOT EXISTS Cards (
        IdCard INTEGER PRIMARY KEY ASC,
        Worker INTEGER NOT NULL,
        FOREIGN KEY(Worker) REFERENCES Workers(IdW)
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS LogsInOut (
        IdL INTEGER PRIMARY KEY ASC,
        Client INTEGER NOT NULL,
        FOREIGN KEY(Client) REFERENCES Clients(IdC),
        Worker INTEGER NOT NULL,
        FOREIGN KEY(Worker) REFERENCES Workers(IdW)
        InOut CHAR NOT NULL,
        DateL DATETIME NOT NULL
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS UnknownUsages (
        IdU INTEGER PRIMARY KEY ASC,
        Card INTEGER NOT NULL,
        FOREIGN KEY(Card) REFERENCES Cards(IdC),
        DateU DATETIME NOT NULL
    )""")
