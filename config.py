import json

GLOBAL_CONFIG = None

def save_config():
    pass

def load_config_file():
    with open("config.json") as cf:
        global GLOBAL_CONFIG
        GLOBAL_CONFIG = json.load(cf)

load_config_file()