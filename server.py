from flask import Flask, render_template, request
import configparser
import os

configFileName = 'config.ini'
app = Flask(__name__)

@app.route("/")
def index():
    dict = {
        'ProtectionMode': config.get('common', "mode"),
        'OpeningTimeCorrection': config.get('auto', "opening_correction"),
        'OpeningTime': config.get('auto', "opening_time"),
        'ClosingMode': config.get('auto', "closing_mode"),
        'ClosingTimeCorrection': config.get('auto', "closing_correction"),
        'ClosingTime': config.get('auto', "closing_time"),
        'ForceDoorStatus': config.get('manual', "manual_mode"),
    }
    return render_template("index.html", config=dict)

@app.route("/save", methods=['POST'])
def save():
    config.set('common', 'mode', request.form["ProtectionMode"])

    config.set('auto', 'opening_mode', request.form['OpeningMode'])
    config.set('auto', 'opening_correction', request.form['OpeningTimeCorrection'])
    config.set('auto', 'opening_time', request.form['OpeningTime'])
    config.set('auto', 'closing_mode', request.form['ClosingMode'])
    config.set('auto', 'closing_correction', request.form['ClosingTimeCorrection'])
    config.set('auto', 'closing_time', request.form['ClosingTime'])

    config.set('manual', 'manual_mode', request.form['ForceDoorStatus'])
    save_config()
    return "saved !"

def save_config():
    with open(configFileName, 'w') as f:
        config.write(f)

def read_config_file():
    config.read(configFileName)
    if not os.path.isfile(configFileName):
        config.add_section('common')
        config.set('common', 'Mode', '1')
        config.set('common', 'Debug', 'false')

        config.add_section('auto')
        config.set('auto', 'opening_mode', '1')
        config.set('auto', 'opening_correction', '0')
        config.set('auto', 'opening_time', '')
        config.set('auto', 'closing_mode', '1')
        config.set('auto', 'closing_correction', '0')
        config.set('auto', 'closing_time', '')

        config.add_section('manual')
        config.set('manual', 'manual_mode', '1')

        save_config()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    read_config_file()

    app.run(host='0.0.0.0', port=80, debug=config.getboolean('common', 'debug'))
