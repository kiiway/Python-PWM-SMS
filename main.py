import sys
import os
import re

import gammu
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gm = gammu.getStateMachine() # Detection du dongle 3G
gm.ReadConfig() # Lecture du fichier de configuration ("/etc/gammurc" & "/etc/gammu-smsdrc")
gm.Init() # Initialisation du dongle

def send_sms(sms_target, sms_content):
    message = {
        'Text': sms_content,
        'Unicode': true,
        'SMSC': {'Location': 1},
        'Number': sms_target,
    }
    gm.SendSMS(message)

def sms_command(sms_content):
    gpio_regex = re.match(r"gpio:([0-9]{1,2});([0-9]{1})", sms_content, re.M|re.I)
    if(gpio_regex):
        gpio.setup(gpio_regex.group(1), gpio.OUT)
        (gpio_regex.group(2)) ? gpio.output(gpio_regex.group(1), gpio.HIGH) : gpio.output(gpio_regex.group(1), gpio.LOW)
        print gpio_regex
        

def main():
    while 1:
        try:
            getSms = sms.GetNextSMS(Location=getSms[0]['Location'], Folder=0)
            print getSms
            sms_command(getSms[0]['Text'], getSms[0]['Number']) #On envoie le contenue du sms a la fonction qui s'occupe des commande par SMS
            sms.DeleteSMS(getSms[0]['Folder'], getSms[0]['Location'])
        except gammu.ERR_EMPTY:
           pass
        sleep(0.150) #On pause le script pendant 150 ms | 0.150 s


if __name__ == '__main__':
    main()
