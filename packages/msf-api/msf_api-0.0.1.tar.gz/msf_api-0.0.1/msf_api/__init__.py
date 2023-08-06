import urllib3

urllib3.disable_warnings()
import json
from .raids import Raid

from .characters.api import MsfCharApi
from .raids.api import MsfRaidApi
from .items.api import MsfItemsApi



class MsfApi:
    def __init__(self, api_key, cache_expiration=None, logger=None, proxy=None):
        self._logger = logger
        self._raids_api = MsfRaidApi(api_key, cache_expiration, logger, proxy)
        self._chars_api = MsfCharApi(api_key, cache_expiration, logger, proxy)
        self._items_api = MsfItemsApi(api_key, cache_expiration, logger, proxy)

    def raids(self):
        return self._raids_api

    def chars(self):
        return self._chars_api

    def items(self):
        return self._items_api

    # higher level methods

    def get_gear_req(self, char_id, from_gear, to_gear):
        """
        returns the total gear cost for a character to get to a gear level from a given level
        :param char_id: character id
        :param from_gear: starting gear level
        :param to_gear: target gear level
        :return: list of gear items
        """
        char_info = self.chars().get_character_info(char_id)
        total_mats = {}
        for gear_level in range(from_gear, to_gear):
            pieces = char_info.get_gear(gear_level)
            for piece in pieces:
                mats = self.items().get_total_material_cost(piece['piece']['id'])
                for item_id, item in mats.items():
                    if item_id not in total_mats:
                        total_mats[item_id] = item
                    else:
                        total_mats[item_id].quantity += item.quantity
        return [{k: v for k, v in item.dict().items() if k in ["id", "name", "icon", "quantity", "tier"]} for
                item_id, item in total_mats.items()]
