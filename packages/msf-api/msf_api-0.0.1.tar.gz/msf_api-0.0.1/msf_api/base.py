import logging
import requests
import requests_cache

from msf_api import Raid


class MsfBaseApi():
    __MSF_API_URL = "https://api.marvelstrikeforce.com/game/v1/"
    __DEFAULT_CACHE_EXPIRATION = 86400

    def __init__(self, api_key, name, cache_expiration=None, api_url=None, logger=None, proxy=None):
        super().__init__()
        self.name = name
        self._logger = logger
        self._api_url = api_url or self.__MSF_API_URL
        self._proxy = {} if proxy is None else {"http": proxy, "https": proxy}
        self._default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self._auth_header = {"x-api-key": api_key}
        requests_cache.install_cache('Msf_{}_cache'.format(name), backend='sqlite',
                                     expire_after=cache_expiration or __DEFAULT_CACHE_EXPIRATION)

    def get_challenges(self):
        return self._get("episodics/challenge")

    def get_raids(self):
        return self._get("raids")

    def get_raid(self, raid_id, nodeInfo="none"):
        raid_data = self._get(f"raids/{raid_id}?nodeInfo={nodeInfo}")
        # save_json("raid_doom1",raid_data)
        return Raid(**raid_data["data"])

    def _get(self, urlpath, params=None, headers=None):
        self._logi(f'[get] URL {urlpath}')
        a_headers = headers or self._default_headers
        a_headers.update(self._auth_header)
        try:
            r = requests.get(f"{self._api_url}{urlpath}",
                             verify=False,
                             params=params or {},
                             proxies=self._proxy,
                             headers=a_headers)
            return r.json()
        except Exception as ex:
            self._loge(ex)

    def _logi(self, msg):
        self._log(logging.INFO, msg)

    def _loge(self, msg):
        self._log(logging.ERROR, msg)

    def _log(self, loglevel, msg):
        if self._logger is not None:
            self._logger.log(loglevel, *msg)

    def test(self):
        self._get("test")
