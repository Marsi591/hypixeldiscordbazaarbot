import json
import os
import shutil

GLOBAL_CONFIG = None
RESPONSES = None
def save_config():
    pass

def load_config_file():
    global GLOBAL_CONFIG, RESPONSES
    if not os.path.isfile("config.json"):
        shutil.copy("example_config.json", "config.json")
        print("A config.json was not found so one has been created.")
    if not os.path.isfile("responses.json"):
        shutil.copy("example_responses.json", "responses.json")
        print("A responses.json was not found so one has been created.")
    with open("config.json") as cf:
        GLOBAL_CONFIG = json.load(cf)
    with open("responses.json") as responses:
        RESPONSES = json.load(responses)
    
load_config_file()