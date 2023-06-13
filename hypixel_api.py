import requests
import json
import time
from config import GLOBAL_CONFIG

def api_request(path, **kwargs):
    return requests.get(GLOBAL_CONFIG["hypixel_api"]["url"] + path, **kwargs).json()

class HypixelApi:
    def __init__(self):
        pass

class Item:
    def __init__(self):
        pass

class Bazaar:
    def __init__(self):
        self.last_update = 0
        self.data = None
    
    def _update_bazaar(self):
        if time.time() - self.last_update > GLOBAL_CONFIG["hypixel_api"]["bazaar"]["poll_rate"]:
            self.data = api_request("skyblock/bazaar")

    @classmethod
    def _ensured(fn):
        def wrapper(self, *args, **kwargs):
            self._update_bazaar()
            fn(self, *args, **kwargs)
        return wrapper
    
    @Bazaar._ensured
    def get_item(self, item_id):
        pass

class AuctionHouse:
    def __init__(self):
        self.last_update = 0
        self.data = None
