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

configFileName = 'config.ini'
webserver = Flask(__name__)
sunrise = sunset = ''


class ProtectionMode(Enum):
    Auto = 1
    Manu = 2


class App(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.a = Astral()
        self.city = self.a['Brussels']

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            # Si en mode auto
            if config.get('common', 'mode') == ProtectionMode.Auto.name:
                sun = self.city.sun(date=datetime.datetime.now(), local=True)
                sunrise = sun['sunrise']
                sunset = sun['sunset']
                correction_opening = config.getint('auto', 'opening_correction')
                correction_closing = config.getint('auto', 'closing_correction')
                opening_mode = config.getint('auto', 'opening_mode')
                closing_mode = config.getint('auto', 'closing_mode')
                opening_time = str.split(config.get('auto', 'opening_time'), ':')
                closing_time = str.split(config.get('auto', 'closing_time'), ':')

                new_sunrise = sunrise + datetime.timedelta(minutes=correction_opening)
                new_sunset = sunset + datetime.timedelta(minutes=correction_closing)

                # if closing_mode == 1:
                if ((closing_mode == 1 and current_time.hour >= new_sunset.hour and current_time.minute >= new_sunset.minute)
                        or (closing_mode == 2 and current_time.hour >= int(closing_time[0]) and current_time.minute >= int(closing_time[1]))):
                    self.close_door()
                elif ((opening_mode == 1 and current_time.hour >= new_sunrise.hour and current_time.minute >= new_sunrise.minute)
                        or (opening_mode == 2 and current_time.hour >= int(opening_time[0]) and current_time.minute >= int(opening_time[1]))):
                    self.open_door()
                else:
                    self.close_door()

            time.sleep(60)

    def close_door(self):
        print('Time to close the door')

    def open_door(self):
        print('Time to open the door')


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

    # Start the thread parallèle
    app = App()
    app.start()

    webserver.run(host='0.0.0.0', port=80, debug=config.getboolean('common', 'debug'))
