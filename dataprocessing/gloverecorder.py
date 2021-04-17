import time
from pynput import keyboard
from glove.gloveHandle import GloveHandle, SourceConfig, Sources

filename = "data/gestures/v/v(20).rec"
#filename = "data/gestures/log/log(18).rec"
file = open(filename, 'wb')
_exit = False
glove = GloveHandle(SourceConfig(Sources.BLUETOOTH, port=1, host="00:21:13:04:d9:63"), nonBlocking=False)


def on_press(key):
    try:
        pass
    except AttributeError:
        pass


def on_release(key):
    global _exit
    if key == keyboard.Key.esc:
        _exit = True
        return False


glove.open()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

print("start saving")
while not _exit:
    file.write(glove._readByteArray(300))
    file.flush()


glove.exit()