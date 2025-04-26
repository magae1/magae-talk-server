import json
from http.client import HTTPSConnection

from settings.config import get_settings


class IceServersClient:
    def __init__(self):
        self.ice_servers = []

    def request_ice_servers(self):
        conn = HTTPSConnection(get_settings().turn_credential_domain)
        try:
            conn.request(
                "GET",
                f"/api/v1/turn/credentials?apiKey={get_settings().turn_credential_api_key}&region=japan",
            )
            res = conn.getresponse()
            self.ice_servers = json.loads(res.read().decode())
        finally:
            conn.close()

    def get_ice_servers(self):
        if len(self.ice_servers) == 0:
            self.request_ice_servers()
        return self.ice_servers
