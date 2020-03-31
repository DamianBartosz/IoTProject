import system
import RFIDSymulator as RFID


def menu():
    print("Menu systemu (wybierz opcje i kliknij Enter):")
    print("1. Wyświetl stan bazy danych")
    print("2. Dodaj pracownika")
    print("3. Przypisz kartę do pracownika")
    print("4. Usuń przypisanie karty do pracownika")
    print("5. Generuj raport dla pracownika")
    print("(Dowolny inny input). Zakończ działanie systemu")


def printClients(clients):
    width = 42
    print('-'*width)
    print("| {:5s} | {:30s} |" .format("ID", "Nazwa"))
    print('*'*width)
    for client in clients:
        print("| {:5d} | {:30s} |"  .format(client['IdC'], client['NameC']))
    print('-'*width)
    print()


def printWorkers(workers):
    width = 68
    print('-'*width)
    print("| {:5s} | {:20s} | {:20s} | {:10s} |" .format(
        "ID", "Imię", "Nazwisko", "Zalogowany"))
    print('*'*width)
    for worker in workers:
        print("| {:5d} | {:20s} | {:20s} | {:10s} |" .format(
            worker['IdW'], worker['FirstName'], worker['LastName'], str(worker['LoggedIn'] == 1)))
    print('-'*width)
    print()


def printCards(cards):
    width = 67
    print('-'*width)
    print("| {:20s} | {:40s} |" .format("ID", "Przypisany pracownik"))
    print('*'*width)
    for card in cards:
        worker = None
        if card['Worker'] != None:
            worker = "%d %s %s" % (
                card['Worker'], card['FirstName'], card['LastName'])
        else:
            worker = str(card['Worker'])
        print("| {:20s} | {:40s} |" .format(card['IdCard'], worker))
    print('-'*width)
    print()


def printLogsInOut(logsInOut):
    width = 131
    print('-'*width)
    print("| {:5s} | {:30s} | {:40s} | {:10s} | {:30s} |".format(
        "ID", "Klient", "Pracownik", "In/Out", "Data"))
    print('*'*width)
    for logInOut in logsInOut:
        worker = "%d %s %s" % (
            logInOut['Worker'], logInOut['FirstName'], logInOut['LastName'])
        print("| {:5d} | {:30s} | {:40s} | {:10s} | {:30s} |" .format(
            logInOut['IdL'], logInOut['NameC'], worker, logInOut['InOut'], logInOut['DateL']))
    print('-'*width)
    print()


def printUnknownUsages(unknownUsages):
    width = 65
    print('-'*width)
    print("| {:5s} | {:20s} | {:30s} |" .format("ID", "Karta", "Data"))
    print('*'*width)
    for unknownUsage in unknownUsages:
        print("| {:5d} | {:20s} | {:30s} |" .format(
            unknownUsage['IdU'], unknownUsage['Card'], unknownUsage['DateU']))
    print('-'*width)
    print()


def dataBaseView():
    base = system.getDataBaseState()

    print("Klienci:")
    printClients(base[0])

    print("Pracownicy:")
    printWorkers(base[1])

    print("Karty:")
    printCards(base[2])

    print("Zalogowania i wylogowania:")
    printLogsInOut(base[3])

    print("Nienznane użycia:")
    printUnknownUsages(base[4])


def addWorkerView():
    print("Podaj imię pracownika: ")
    firstName = input()
    print("Podaj nazwisko pracownika: ")
    lastName = input()

    workers = system.newWorker(firstName, lastName)

    print("Pracownik %s %s dodany do bazy." % (firstName, lastName))
    print("Aktualna lista pracowników: ")
    printWorkers(workers)


def checkCardView():
    print("Przyłóż kartę do czytnika")
    return RFID.setUnsetCard()


def generateRaportView():
    printWorkers(system.getWorkersList())
    print("Podaj ID pracownika, dla którego chcesz wygenerować raport")
    workerId = input()
    system.generateRaport(workerId)


def main():
    loop = True
    while loop:
        menu()
        x = input()
        if x == '1':
            dataBaseView()
        elif x == '2':
            addWorkerView()
        elif x == '3':
            cardId = checkCardView()
            printWorkers(system.getWorkersList())
            print("Podaj ID pracownika, do którego chcesz przypisać kartę")
            workerId = input()
            system.setCard(cardId, workerId)
            print("Przypisano kartę")
        elif x == '4':
            cardId = checkCardView()
            system.unsetCard(cardId)
            print("Usunięto przypisanie karty")
        elif x == '5':
            generateRaportView()
        else:
            system.closeDB()
            loop = False


if __name__ == "__main__":
    main()
