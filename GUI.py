import system
import DBPackage.DBService as api
from tkinter import *  # pylint: disable=unused-wildcard-import
from tkinter import ttk

window = Tk()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def createMainWindow():
    window.title("System logowania pracowników")

    topFrame = Frame(window)
    mainFrame = Frame(window)
    bottomFrame = Frame(window)

    menuLabel = Label(topFrame, text="Menu")

    clientsButton = Button(
        mainFrame, text="Zarządzanie klientami", command=clientsManagment)
    workersButton = Button(
        mainFrame, text="Zarządzanie pracownikami", command=workersManagement)
    cardsButton = Button(
        mainFrame, text="Zarządzanie kartami", command=cardsManagement)
    logsButton = Button(
        mainFrame, text="Przeglądanie logowań", command=logsView)
    ukUsagesButton = Button(
        mainFrame, text="Przeglądanie nieznanych użyć", command=ukUsagesView)
    reportButton = Button(
        mainFrame, text="Generowanie raportu", command=generateReport)

    exitButton = Button(bottomFrame, text="Stop", command=window.destroy)

    topFrame.pack(side=TOP)
    mainFrame.pack()
    bottomFrame.pack(side=BOTTOM)
    menuLabel.pack()
    clientsButton.pack()
    workersButton.pack()
    cardsButton.pack()
    logsButton.pack()
    ukUsagesButton.pack()
    reportButton.pack()
    exitButton.pack(side=RIGHT)


def clientsManagment():
    clients = api.getClientsList()

    clientsWindow = Tk()
    clientsWindow.title("Zarządzanie klientami")
    infoLabel = Label(clientsWindow, text="Baza klientów:")
    infoLabel.pack()

    clientsFrame = ScrollableFrame(clientsWindow)
    clientsFrame.pack()

    Button(clientsWindow, text="+", fg="green",
           command=lambda: addClientWindow(clientsFrame.scrollable_frame)).pack(side=TOP)

    for client in clients:
        showClient(client, clientsFrame.scrollable_frame)

    clientsWindow.mainloop()


def showClient(client, clientsFrame):

    clientFrame = Frame(clientsFrame)
    Label(clientFrame, text=client['IdC']).grid(column=0, row=0)
    Label(clientFrame, text=client['NameC']).grid(column=1, row=0)
    Button(clientFrame, text="Usuń",
           command=lambda id=client['IdC'], cFrame=clientFrame: deleteClient(id, cFrame)).grid(column=2, row=0)
    clientFrame.pack()


def addClientWindow(clientsFrame):
    addingWindow = Tk()
    addingWindow.title("Dodaj klienta")

    Label(addingWindow, text="Podaj nazwę klienta RFID").grid(row=0, column=0)

    nameEntry = Entry(addingWindow)
    nameEntry.grid(row=0, column=1)

    Button(addingWindow, text="Zakończ",
           command=addingWindow.destroy).grid(row=1, column=0)

    Button(addingWindow, text="Zatwierdź",
           command=lambda: addClient(nameEntry.get(), clientsFrame)).grid(row=1, column=1)

    addingWindow.mainloop()


def addClient(name, frame):
    newClient = api.addClient(name)
    system.generateTerminalCode(newClient['NameC'], newClient['IdC'])

    showClient(newClient, frame)


def deleteClient(id, cFrame):
    cFrame.destroy()
    api.deleteClient(id)


def workersManagement():
    workers = api.getWorkersList()

    workersWindow = Tk()
    workersWindow.title("Zarządzanie pracownikami")
    Label(workersWindow, text="Baza pracowników:").pack()

    workersFrame = ScrollableFrame(workersWindow)
    workersFrame.pack()

    Button(workersWindow, text="+", fg="green",
           command=lambda: addWorkerWindow(workersFrame.scrollable_frame)).pack(side=TOP)

    for worker in workers:
        showWorker(worker, workersFrame.scrollable_frame)

    workersWindow.mainloop()


def addWorkerWindow(workersFrame):
    addingWindow = Tk()
    addingWindow.title("Dodaj pracownika")

    Label(addingWindow, text="Podaj imię pracownika").grid(row=0, column=0)

    firstNameEntry = Entry(addingWindow)
    firstNameEntry.grid(row=0, column=1)

    Label(addingWindow, text="Podaj nazwisko pracownika").grid(row=1, column=0)

    lastNameEntry = Entry(addingWindow)
    lastNameEntry.grid(row=1, column=1)

    Button(addingWindow, text="Zakończ",
           command=addingWindow.destroy).grid(row=2, column=0)

    Button(addingWindow, text="Zatwierdź",
           command=lambda: addWorker(firstNameEntry.get(), lastNameEntry.get(), workersFrame)).grid(row=2, column=1)

    addingWindow.mainloop()


def addWorker(firstName, lastName, frame):
    newWorker = api.addWorker(firstName, lastName)

    showWorker(newWorker, frame)


def showWorker(worker, workersFrame):

    workerFrame = Frame(workersFrame)
    Label(workerFrame, text=worker['IdW']).grid(column=0, row=0)
    Label(workerFrame, text=worker['FirstName']).grid(column=1, row=0)
    Label(workerFrame, text=worker['LastName']).grid(column=2, row=0)
    loggedIn = ""
    if worker['LoggedIn'] == 0:
        loggedIn = "Wylogowany"
    else:
        loggedIn = "Zalogowany"
    Label(workerFrame, text=loggedIn).grid(column=3, row=0)
    workerFrame.pack()


def cardsManagement():
    cards = api.getCardsList()

    cardsWindow = Tk()
    cardsWindow.title("Zarządzanie kartami")
    Label(cardsWindow, text="Baza kart:").pack()

    cardsFrame = ScrollableFrame(cardsWindow)
    cardsFrame.pack()

    for card in cards:
        showCard(card, cardsFrame.scrollable_frame)

    cardsWindow.mainloop()


def showCard(card, cardsFrame):
    cardFrame = Frame(cardsFrame)
    Label(cardFrame, text=card['IdCard']).grid(column=0, row=0)
    workerFrame = Frame(cardFrame)
    if card['Worker'] != None:
        Label(workerFrame, text=card['Worker']).grid(column=0, row=0)
        Label(workerFrame, text=card['FirstName']).grid(column=1, row=0)
        Label(workerFrame, text=card['LastName']).grid(column=2, row=0)
    else:
        Label(workerFrame, text="Nie przypisano").grid(column=0, row=0)
    workerFrame.grid(column=1, row=0)

    Button(cardFrame, text="Przypisz pracownika",
           command=lambda: asignWorker(card['IdCard'], workerFrame)).grid(column=2, row=0)

    cardFrame.pack()


def asignWorker(cardId, workerFrame):
    selectedWorker = selectWorker(True)

    if str(selectedWorker) == "0":
        api.setCard(cardId, None)
        for wid in workerFrame.winfo_children():
            wid.destroy()
        Label(workerFrame, text="Nie przypisano").grid(column=0, row=0)
    elif str(selectedWorker) == "-1":
        return
    else:
        api.setCard(cardId, selectedWorker)
        for wid in workerFrame.winfo_children():
            wid.destroy()
        card = api.getCardWorker(cardId)
        Label(workerFrame, text=card['Worker']).grid(column=0, row=0)
        Label(workerFrame, text=card['FirstName']).grid(column=1, row=0)
        Label(workerFrame, text=card['LastName']).grid(column=2, row=0)


def selectWorker(noneSelectOption):

    workersWindow = Tk()
    workersWindow.title("Wybór pracownika")

    Label(workersWindow, text="Wybierz pracownika:").pack()
    selectedWorker = [-1]
    workers = api.getWorkersList()

    scrFrame = ScrollableFrame(workersWindow)
    scrFrame.pack()

    workersFrame = scrFrame.scrollable_frame

    for worker in workers:
        workerFrame = Frame(workersFrame)
        Label(workerFrame, text=worker['IdW']).grid(column=0, row=0)
        Label(workerFrame, text=worker['FirstName']).grid(column=1, row=0)
        Label(workerFrame, text=worker['LastName']).grid(column=2, row=0)
        Button(workerFrame, text="Wybierz pracownika",
               command=lambda workerId=worker['IdW']: selectButtonOnClick(workerId, selectedWorker, workersWindow)).grid(column=3, row=0)
        workerFrame.pack()

    if noneSelectOption:
        Button(workersFrame, text="Brak pracownika",
               command=lambda: selectButtonOnClick(0, selectedWorker, workersWindow)).pack()

    workersFrame.pack()

    Button(workersWindow, text="Anuluj", command=workersWindow.destroy).pack()

    workersWindow.wait_window()
    return selectedWorker[0]


def selectButtonOnClick(workerId, selectedWorker, workersWindow):
    selectedWorker[0] = workerId
    workersWindow.destroy()


def logsView():
    logs = api.getLogsInOutList()

    logsWindow = Tk()
    logsWindow.title("Przeglądanie logowań")
    Label(logsWindow, text="Baza logowań:").pack()

    logsFrame = ScrollableFrame(logsWindow)
    logsFrame.pack()

    for log in logs:
        showLog(log, logsFrame.scrollable_frame)

    logsWindow.mainloop()


def showLog(log, frame):
    logFrame = Frame(frame)
    Label(logFrame, text=log['IdL']).grid(column=0, row=0)
    Label(logFrame, text=log['Client']).grid(column=1, row=0)
    Label(logFrame, text=log['NameC']).grid(column=2, row=0)
    Label(logFrame, text=log['Worker']).grid(column=3, row=0)
    Label(logFrame, text=log['FirstName']).grid(column=4, row=0)
    Label(logFrame, text=log['LastName']).grid(column=5, row=0)
    Label(logFrame, text=log['InOut']).grid(column=6, row=0)
    Label(logFrame, text=log['DateL']).grid(column=7, row=0)

    logFrame.pack()


def ukUsagesView():
    ukUsages = api.getUnknownUsagesList()

    ukUsagesWindow = Tk()
    ukUsagesWindow.title("Przeglądanie nieznnych użyć")
    Label(ukUsagesWindow, text="Baza nieznanych użyć:").pack()

    ukUsagesFrame = ScrollableFrame(ukUsagesWindow)
    ukUsagesFrame.pack()

    for ukUsage in ukUsages:
        showUkUsage(ukUsage, ukUsagesFrame.scrollable_frame)

    ukUsagesWindow.mainloop()


def showUkUsage(ukUsage, frame):
    ukUsageFrame = Frame(frame)
    Label(ukUsageFrame, text=ukUsage['IdU']).grid(column=0, row=0)
    Label(ukUsageFrame, text=ukUsage['Client']).grid(column=1, row=0)
    Label(ukUsageFrame, text=ukUsage['NameC']).grid(column=2, row=0)
    Label(ukUsageFrame, text=ukUsage['Card']).grid(column=3, row=0)
    Label(ukUsageFrame, text=ukUsage['DateU']).grid(column=4, row=0)

    ukUsageFrame.pack()


def generateReport():
    selectedWorker = selectWorker(False)

    if str(selectedWorker) != "-1":
        system.generateReport(selectedWorker)


def runGUI():
    system.start()
    createMainWindow()
    window.mainloop()
    system.close()


if __name__ == "__main__":
    runGUI()
