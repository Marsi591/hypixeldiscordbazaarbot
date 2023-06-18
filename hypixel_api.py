import requests
import json
import time
from config import GLOBAL_CONFIG

def api_request(path, **kwargs):
    return requests.get(GLOBAL_CONFIG["hypixel_api"]["url"] + path, **kwargs).json()

class HypixelApi:
    def __init__(self):
        self._items_obj
        self._bazaar_obj
        self._auction_house_obj

    @property
    def items(self):
        if self._items_obj.is_aged:
            self._items_obj = _get_items()
        return self._items_obj

    def _get_items(self):
        return Items()

    @property
    def bazaar(self):
        pass

    def _get_bazaar(self):
        return Bazaar()

    @property
    def auction_house(self):
        pass

    def _get_auction_house(self):
        
        return AuctionHouse()

class AgingMixin:
    def __init__(self, max_age, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation_date = time.time()
        self.max_age = max_age

    @property
    def is_aged():
        return time.time() - creation_date >= self.max_age

class Items(AgingMixin):
            def __init__(self, hypixel_api):
                super().__init__(GLOBAL_CONFIG["items"]["poll_rate"])
                pass

class Bazaar(AgingMixin):
            def __init__(self, hypixel_api):
                pass

class AuctionHouse(AgingMixin):
            def __init__(self, hypixel_api):
                pass

class Item:
    pass

class BazaarItem(Item):
    pass

class AuctionableItem(Item):
    pass