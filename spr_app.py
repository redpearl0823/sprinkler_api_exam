import requests
import logging

from spr_api.spr_auth import SprAuth
from spr_api.spr_auth import DEFAULT_BASE_URL

logger = logging.getLogger("apr_app")


class SprApp:
    """
    Application object used to make api calls.
    """

    def __init__(self, base_url=DEFAULT_BASE_URL, env=None, key=None, secret=None, redirect_uri=None, username=None,
                 password=None, auth_code=None):
        self.base_url = base_url
        self.spr_auth = SprAuth(env, key, secret, redirect_uri, username=username, password=password,
                                auth_code=auth_code)

    def request(self, method, endpoint, params=None, headers=None, data=None):
        """
        Adds the Auth Headers and makes api call. If auth token is invalid, it is refreshed.
        Returns the response from api call.
        """

        # initial default parameters
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        # adding auth headers
        if not "Authorization" in headers:
            headers["Authorization"] = "Bearer {}".format(self.spr_auth.access_token)
        if not "Key" in headers:
            headers["Key"] = self.spr_auth.key

        # Adding base url to the endpoint
        base_url = self.base_url
        if self.spr_auth.env != 'prod':
            base_url = base_url + self.spr_auth.env + "/"
        endpoint = base_url + "api/v2/" + endpoint

        response = requests.request(method, endpoint, headers=headers, data=data, params=params)
        if response.status_code == 401:
            self.spr_auth.gen_access_token_from_refresh_token()
            response = requests.request(method, endpoint, headers=headers, data=data, params=params)

        try:
            response.json()
        except ValueError as e:
            # handles non-json responses (e.g. HTTP 404, 500, 502, 503, 504)
            if "Expecting value: line 1 column 1 (char 0)" in str(e):
                logger.error(
                    "There was an error with this request: \n{}\n{}\n{}".format(
                        response.url, data, response.text
                    )
                )
                raise RuntimeError(response.text)
            else:
                raise
        else:
            if "errors" in response.json() and response.json()["errors"]:
                logger.error(
                    "There was an error with this request: \n{}\n{}\n{}".format(
                        response.url, data, response.json()["errors"]
                    )
                )
                raise RuntimeError(response.json()["errors"])

        return response.json()["data"]
