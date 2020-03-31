# -*- coding: utf-8 -*-

import sqlite3

# connect to base
con = sqlite3.connect('SystemDB.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

# base model
cur.execute("""
    CREATE TABLE IF NOT EXISTS Workers (
        IdW INTEGER PRIMARY KEY ASC,
        FirstName varchar(30) NOT NULL,
        LastName varchar(30) NOT NULL,
        LoggedIn BIT NOT NULL
    )""")

cur.executescript("""
    CREATE TABLE IF NOT EXISTS Clients (
        IdC INTEGER PRIMARY KEY ASC,
        NameC varchar(30) NOT NULL
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Cards (
        IdCard varchar(30) PRIMARY KEY ASC,
        Worker INTEGER NULL,
        FOREIGN KEY (Worker) REFERENCES Workers(IdW)
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS LogsInOut (
        IdL INTEGER PRIMARY KEY ASC,
        Client INTEGER NOT NULL,
        Worker INTEGER NOT NULL,
        InOut CHAR NOT NULL,
        DateL DATETIME NOT NULL,
        FOREIGN KEY (Client) REFERENCES Clients(IdC),
        FOREIGN KEY (Worker) REFERENCES Workers(IdW)
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS UnknownUsages (
        IdU INTEGER PRIMARY KEY ASC,
        Card varchar(30) NOT NULL,
        DateU DATETIME NOT NULL,
        FOREIGN KEY (Card) REFERENCES Cards(IdC)
    )""")
