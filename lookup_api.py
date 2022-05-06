import json

from spr_api.spr_app import SprApp
from spr_api.endpoints import LOOKUP_ENDPOINT


class LookupRequest():

    def __init__(self):
        self.keys = []

    def type(self, lookupType):
        self.lookupType = lookupType

    def add_key(self, key):
        self.keys.append(key)

    def add_keys(self, keys):
        self.keys.extend(keys)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class LookupApi:

    def __init__(self, app: SprApp):
        self.app = app
        if app is None:
            raise TypeError("app can't be None")

    def lookup(self, lookup_request: LookupRequest):
        """

        Returns
        -------
        dict - consisting response for each key in lookup request
        """
        headers = {
            "Content-Type": "application/json"
        }
        return self.app.request("POST", LOOKUP_ENDPOINT, headers=headers, data=lookup_request.toJson(), params={})
