import json

GLOBAL_CONFIG = None
RESPONSES = None
def save_config():
    pass

def load_config_file():
    global GLOBAL_CONFIG, RESPONSES
    with open("config.json") as cf:
        GLOBAL_CONFIG = json.load(cf)
    with open("responses.json") as responses:
        RESPONSES = json.load(responses)
    

load_config_file()