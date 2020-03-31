from pynput import keyboard
import system

clientId = 1


def main():
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                break
            elif str(type(event)) == "<class 'pynput.keyboard.Events.Press'>" and str(type(event.key)) == "<class 'pynput.keyboard._win32.KeyCode'>":
                num = ord(event.key.char)
                num = num << 32
                worker = system.RFIDHandler(clientId, num)
                if worker == None:
                    print("Brak dostępu")
                elif worker['LoggedIn'] == 0:
                    print("Witaj %s %s" %
                          (worker['FirstName'], worker['LastName']))
                else:
                    print("Do zobaczenia %s %s" %
                          (worker['FirstName'], worker['LastName']))


def setUnsetCard():
    with keyboard.Events() as events:
        event = events.get()
        if str(type(event)) == "<class 'pynput.keyboard.Events.Press'>" and str(type(event.key)) == "<class 'pynput.keyboard._win32.KeyCode'>":
            num = ord(event.key.char)
            num = num << 32
            return num
        else:
            return setUnsetCard()


if __name__ == "__main__":
    main()
