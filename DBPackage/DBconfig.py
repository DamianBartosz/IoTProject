#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

# connect to base


def createDB():
    if os.path.exists("SystemDB.db"):
        os.remove("SystemDB.db")
        print("An old database removed.")

    con = sqlite3.connect('SystemDB.db')
    cur = con.cursor()

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
            Client INTEGER NOT NULL,
            Card varchar(30) NOT NULL,
            DateU DATETIME NOT NULL,
            FOREIGN KEY (Client) REFERENCES Clients(IdC),
            FOREIGN KEY (Card) REFERENCES Cards(IdC)
        )""")

    cur.execute('INSERT INTO Clients VALUES(NULL, ?);',
                ("Klient został usunięty",))

    con.commit()
    con.close()
    print("The new database created.")


if __name__ == "__main__":
    createDB()
