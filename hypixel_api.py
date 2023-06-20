import requests
import json
import time
from config import GLOBAL_CONFIG


class HypixelApi:
    def __init__(self):
        self._items_obj = Items(self)
        self._bazaar_obj = Bazaar(self)
        self._auction_house_obj = None

    def request(self, path, **kwargs):
        return requests.get(GLOBAL_CONFIG["hypixel_api"]["url"] + path, **kwargs).json()

    @property
    def items(self):
        if self._items_obj.is_aged():
            print("The item database was out of date, refetching...")
            self._items_obj = Items(self)
        return self._items_obj

    @property
    def bazaar(self):
        if self._bazaar_obj.is_aged():
            print("The bazaar database was out of date, refetching...")
            self._bazaar_obj = Bazaar(self)
        return self._bazaar_obj

    @property
    def auction_house(self):
        if self._auction_house_obj.is_aged():
            print("The auction house database was out of date, refetching...")
            self._auction_house_obj = AuctionHouse()
        return self._auction_house_object


class AgingMixin:
    def __init__(self, max_age, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation_date = time.time()
        self.max_age = int(max_age)

    def is_aged(self):
        return time.time() - self.creation_date >= self.max_age


class ApiComponentMixin:
    def __init__(self, hypixel_api, api_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = hypixel_api
        self.api_path = api_path
        self.raw_data = self.api.request(self.api_path)


class Items(ApiComponentMixin, AgingMixin):
    def __init__(self, hypixel_api):
        super().__init__(hypixel_api, "resources/skyblock/items",
                         GLOBAL_CONFIG["hypixel_api"]["items"]["poll_rate"])
        self.item_ids = self._get_item_ids()
        self.items_dict = self._create_items_dict()

    def _get_item_ids(self):
        item_id_list = []
        for i in self.raw_data["items"]:
            item_id_list.append(i["id"])
        return item_id_list

    def _create_items_dict(self):
        return dict(zip(self.item_ids, self.raw_data["items"]))

    def _create_item_obj(self, item_id):
        if item_id in self.api.bazaar.item_ids:
            return BazaarItem(self.items_dict[item_id], self.api.bazaar.items_dict[item_id])
        else:
            return Item(self.items_dict[item_id])

    def get_item_by_id(self, item_id):
        if item_id in self.item_ids:
            return self._create_item_obj(item_id)
        else:
            raise ValueError(f"Invalid item id {item_id}")


class Bazaar(ApiComponentMixin, AgingMixin):
    def __init__(self, hypixel_api):
        super().__init__(hypixel_api, "skyblock/bazaar",
                         GLOBAL_CONFIG["hypixel_api"]["bazaar"]["poll_rate"])
        self.item_ids = self._get_item_ids()
        self.items_dict = self._create_items_dict()
        self.property_list = [
            "sellPrice",
            "sellVolume",
            "sellMovingWeek",
            "sellOrders",
            "buyPrice",
            "buyVolume",
            "buyMovingWeek",
            "buyOrders",
            "margin",
            "percentMargin"
        ]

    def _create_items_dict(self):
        return self.raw_data["products"]

    def _get_item_ids(self):
        return [x for x in self.raw_data["products"] if not ("ENCHANTMENT" in x or "ESSENCE" in x or x == "BAZAAR_COOKIE")]

    def limit_search(self):
        return BazaarLimitSearch(self)

    def _do_limit_search(self, bazaar_search):
        results = []
        for item_id in self.item_ids:
            product_item = self.api.items.get_item_by_id(item_id)
            all_match = True
            for limit in bazaar_search.limits:
                if limit["less_than"]:
                    if not (product_item.get_bazaar_property(limit["property"]) < limit["value"]):
                        all_match = False
                        break
                elif not limit["less_than"]:
                    if not (product_item.get_bazaar_property(limit["property"]) > limit["value"]):
                        all_match = False
                        break
            if all_match:
                results.append(product_item)
        return results

    def max_search(self, property_name):
        if property_name in self.property_list:
            result = self.raw_data["products"][0]
            for product in self.raw_data["products"]:
                if result[property_name] < product[property_name]:
                    result = product
            return self.api.get_item_by_id(result["product_id"])
        else:
            raise ValueError("Invalid property to search by")

    def min_search(self, property_name):
        if property_name in self.property_list:
            result = self.raw_data["products"][0]
            for product in self.raw_data["products"]:
                if result[property_name] > product[property_name]:
                    result = product
            return self.api.get_item_by_id(result["productId"])
        else:
            raise ValueError("Invalid property to search by")


class BazaarLimitSearch:
    def __init__(self, bazaar):
        self.bazaar = bazaar
        self.limits = []

    def add_limit(self, property_name, less_than, value):
        if property_name in self.bazaar.property_list:
            self.limits.append({
                "property": property_name,
                "less_than": less_than,
                "value": value
            })
        else:
            ValueError("Invalid property to search by")

    def finalize(self):
        return self.bazaar._do_limit_search(self)


class AuctionHouse(AgingMixin):
    def __init__(self, hypixel_api):
        super().__init__(GLOBAL_CONFIG["items"]["poll_rate"])
        self.raw_data = self.api.request("skyblock/auction")


class Item:
    def __init__(self, raw_data):
        self.last_updated = time.time()
        self.raw_data = raw_data
        self.build_item()

    def build_item(self):
        self.id = self.raw_data["id"]
        self.name = self.raw_data["name"]
        self.material = self.raw_data["material"]
        self.is_in_bazaar = False
        self.is_in_auction_house = False


class BazaarItem(Item):
    def __init__(self, raw_data, bz_data):
        super().__init__(raw_data)
        self.bz_data = bz_data
        self.build_bazaar_item()

    def build_bazaar_item(self):
        quick_status = self.bz_data["quick_status"]
        self.bz_price = {
            "buy": quick_status["buyPrice"],
            "sell": quick_status["sellPrice"],
            "margin": quick_status["buyPrice"] - quick_status["sellPrice"],
            #"percent_margin": (quick_status["buyPrice"] - quick_status["sellPrice"]) / quick_status["buyPrice"]
        }
        self.bz_volume = {
            "buy": quick_status["buyVolume"],
            "sell": quick_status["sellVolume"]
        }
        self.bz_moving_week = {
            "buy": quick_status["buyMovingWeek"],
            "sell": quick_status["sellMovingWeek"]
        }
        self.bz_order_count = {
            "buy": quick_status["buyOrders"],
            "sell": quick_status["sellOrders"]
        }
        self.bz_orders = {
            "buy": self.bz_data["buy_summary"],
            "sell": self.bz_data["sell_summary"],
        }
        self.is_in_bazaar = True

    def get_bazaar_property(self, property_name):
        quick_status = self.bz_data["quick_status"]
        if property_name in list(quick_status.keys()):
            return quick_status[property_name]
        #elif property_name == "percentMargin":
        #    return self.bz_price["percent_margin"]
        elif property_name == "margin":
            return self.bz_price["margin"]


class AuctionableItem(Item):
    pass
