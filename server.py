#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from threading import Thread
from enum import Enum
import configparser
import os
import time
import datetime
from astral import Astral
import RPi.GPIO as GPIO

configFileName = 'config.ini'
webserver = Flask(__name__)

a = Astral()
city = a['Brussels']


class ProtectionMode(Enum):
    Auto = 1
    Manu = 2


def run():
    while True:
        current_time = datetime.datetime.now()
        # Si en mode auto
        if config.get('common', 'mode') == ProtectionMode.Auto.name:
            opening_mode = config.getint('auto', 'opening_mode')
            closing_mode = config.getint('auto', 'closing_mode')
            opening_time = str.split(config.get('auto', 'opening_time'), ':')
            closing_time = str.split(config.get('auto', 'closing_time'), ':')

            auto_closing_time = get_closing_datetime()
            auto_opening_time = get_opening_datetime()

            if ((closing_mode == 1 and current_time.hour >= auto_closing_time.hour and current_time.minute >= auto_closing_time.minute)
                    or (closing_mode == 2 and current_time.hour >= int(closing_time[0]) and current_time.minute >= int(closing_time[1]))):
                close_door()
            elif ((opening_mode == 1 and current_time.hour >= auto_opening_time.hour and current_time.minute >= auto_opening_time.minute)
                    or (opening_mode == 2 and current_time.hour >= int(opening_time[0]) and current_time.minute >= int(opening_time[1]))):
                open_door()
            else:
                close_door()
        else:
            mode = config.getint('manual', 'manual_mode')
            if mode == 1:
                close_door()
            else:
                open_door()

        time.sleep(60)


def close_door():
    GPIO.output(config.getint('common', 'pin_number'), GPIO.LOW)


def open_door():
    GPIO.output(config.getint('common', 'pin_number'), GPIO.HIGH)


def get_sunrise():
    sun = city.sun(date=datetime.datetime.now(), local=True)
    return sun['sunrise']


def get_sunset():
    sun = city.sun(date=datetime.datetime.now(), local=True)
    return sun['sunset']


def get_opening_datetime():
    correction_opening = config.getint('auto', 'opening_correction')
    return get_sunrise() + datetime.timedelta(minutes=correction_opening)


def get_closing_datetime():
    correction_closing = config.getint('auto', 'closing_correction')
    return get_sunset() + datetime.timedelta(minutes=correction_closing)


@webserver.route("/")
def index():
    dict = {
        'ProtectionMode': config.get('common', "mode"),
        'OpeningMode': config.get('auto', "opening_mode"),
        'OpeningTimeCorrection': config.get('auto', "opening_correction"),
        'OpeningTime': config.get('auto', "opening_time"),
        'ClosingMode': config.get('auto', "closing_mode"),
        'ClosingTimeCorrection': config.get('auto', "closing_correction"),
        'ClosingTime': config.get('auto', "closing_time"),
        'ForceDoorStatus': config.get('manual', "manual_mode"),
        'sunrise': {
            'hour': get_opening_datetime().hour,
            'minute': "%02d" % get_opening_datetime().minute
        },
        'sunset': {
            'hour': get_closing_datetime().hour,
            'minute': "%02d" % get_closing_datetime().minute
        }
    }
    return render_template("index.html", config=dict)


@webserver.route("/save", methods=['POST'])
def save():
    config.set('common', 'mode', request.form["ProtectionMode"])

    config.set('auto', 'opening_mode', request.form['OpeningMode'])
    config.set('auto', 'opening_correction', request.form['OpeningTimeCorrection'])
    config.set('auto', 'opening_time', request.form['OpeningTime'] if request.form['OpeningTime'] != '' else '00:00')
    config.set('auto', 'closing_mode', request.form['ClosingMode'])
    config.set('auto', 'closing_correction', request.form['ClosingTimeCorrection'])
    config.set('auto', 'closing_time', request.form['ClosingTime'] if request.form['ClosingTime'] != '' else '23:59')

    config.set('manual', 'manual_mode', request.form['ForceDoorStatus'])
    save_config()
    return "saved"


def save_config():
    with open(configFileName, 'w') as f:
        config.write(f)


def read_config_file():
    config.read(configFileName)
    if not os.path.isfile(configFileName):
        config.add_section('common')
        config.set('common', 'Mode', ProtectionMode.Auto.name)
        config.set('common', 'Debug', 'false')
        config.set('common', 'pin_number', '28')

        config.add_section('auto')
        config.set('auto', 'opening_mode', '1')
        config.set('auto', 'opening_correction', '0')
        config.set('auto', 'opening_time', '00:00')
        config.set('auto', 'closing_mode', '1')
        config.set('auto', 'closing_correction', '0')
        config.set('auto', 'closing_time', '23:59')

        config.add_section('manual')
        config.set('manual', 'manual_mode', '1')

        save_config()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    read_config_file()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.getint('common', 'pin_number'), GPIO.OUT)

    # Start the thread parallèle
    app = Thread(target=run)
    app.start()

    webserver.run(host='0.0.0.0', port=80, debug=config.getboolean('common', 'debug'))
