import sys
import os
import re
from time import sleep

import gammu
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gm = gammu.getStateMachine()
gm.ReadConfig()
gm.Init()

def send_sms(sms_target, sms_content):
    message = {
        'Text': sms_content,
        'Unicode': True,
        'SMSC': {'Location': 1},
        'Number': sms_target,
    }
    gm.SendSMS(message)

def sms_command(sms_content):
    pwm_regex = re.match(r"pwm:([0-9]{2,3});([0-9]{0,2});([0-9]{3});([0-9]{0,2})", sms_content, re.M|re.I)
    if(pwm_regex):
        pwm_freq     = int(pwm_regex.group(1))
        pwm_dt_cycle = int(pwm_regex.group(2))
        pwm_sleep    = float(pwm_regex.group(3))
        pwm_channel  = int(pwm_regex.group(4))
        gpio.setup(pwm_channel,gpio.OUT)
        pwm = gpio.PWM(pwm_channel,pwm_freq)
        pwm.start(0)
        print pwm_regex


def main():
    while 1:
        try:
            getSms = gm.GetNextSMS(Start=True, Folder=0)
            #getSms = gm.GetNextSMS(Location=getSms[0]['Location'], Folder=0)
            sms_command(getSms[0]['Text'])
            gm.DeleteSMS(getSms[0]['Folder'], getSms[0]['Location'])
        except gammu.ERR_EMPTY:
            pass
        sleep(0.150)

if __name__ == '__main__':
    main()
