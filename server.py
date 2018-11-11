from flask import Flask, render_template, request
import configparser
import os

configFileName = 'config.ini'

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/save", methods=['POST'])
def save():
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
