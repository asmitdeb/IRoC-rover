from pynput import keyboard

keys = []

command = {"w": "moving forward", "a": "turning left", "s": "moving backwards", "d": "moving right"}

def on_press(key):
    if not keys:
        instruction = key.char
        keys.append(instruction)
        print(command[instruction])
        # execute command to move

def on_release(key):
    if keys:
        print("stopped")
        # execute command to stop
        keys.clear()
    

# Collect events until released
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

keyboard_listener.start()
keyboard_listener.join()
