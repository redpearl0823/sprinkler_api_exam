import requests
from urllib.parse import quote_plus
import time

from .credentials import CredentialsFile
from .endpoints import DEFAULT_BASE_URL, OAUTH_PATH

class SprAuth:
    """
    Application object which handles authentication required to make api calls to sprinklr.
    """

    def __init__(self, env=None, key=None, secret=None, redirect_uri=None, username=None, password=None,
                 auth_code=None):
        """
               Parameters
               ----------
               env : str
                   Enviroment for which key is generated, eg:- prod1, qa4
               key : str
                   Key corresponding to the mashery application
               secret : str
                   Secret correspoding to the mashery application
               redirect_uri : str
                   Redirect Uri corresponding to the mashery application
               username:str, to be passed when using password authentication
                   Sprinklr Email Address
               password:str, to be passed when using password authentication
                   Sprinklr Password
               auth_code : str, optional, to be used when using oauth
                   One time authorization code generated for creating the access token. Auth Code is valid only for 10 min.
               """

        self.base_url = DEFAULT_BASE_URL
        self.credentials_file = CredentialsFile()
        auth_dict = self.credentials_file.read_file()

        if env is None and key is None:
            if len(auth_dict) == 0:
                raise RuntimeError("Please authenticate using password_auth or oauth")
            else:
                self.env = list(auth_dict.keys())[0]
                self.key = list(auth_dict[self.env].keys())[0]
        else:
            self.env = env
            self.key = key

        # auth using auth code
        if (secret is not None) and (redirect_uri is not None) and (auth_code is not None):
            self.secret = secret
            self.redirect_uri = redirect_uri
            self.auth_code = auth_code
            response = self._gen_auth()
            self.access_token, self.refresh_token = response["access_token"], response["refresh_token"]
            self.expires_at = time.time() + response["expires_in"]
            self.credentials_file.update_key(
                key=self.key, env=self.env, secret=self.secret, redirect_uri=self.redirect_uri,
                refresh_token=self.refresh_token, access_token=self.access_token, expires_at=self.expires_at)
        # auth using username and password
        elif (secret is not None) and (redirect_uri is not None) and (username is not None) and (password is not None):
            self.secret = secret
            self.redirect_uri = redirect_uri
            self.username = username
            self.password = password
            response = self._gen_pass_auth()
            self.access_token, self.refresh_token = response["access_token"], response["refresh_token"]
            self.expires_at = time.time() + response["expires_in"]
            self.credentials_file.update_key(
                key=self.key, env=self.env, secret=self.secret, redirect_uri=self.redirect_uri,
                refresh_token=self.refresh_token, access_token=self.access_token, expires_at=self.expires_at)
        # find creds for env and key
        else:
            key_exists = False
            if self.env in auth_dict:
                if self.key in auth_dict[self.env]:
                    key_exists = True
                    key_dict = auth_dict[self.env][self.key]
                    self.access_token = key_dict['access_token']
                    self.refresh_token = key_dict['refresh_token']
                    self.expires_at = key_dict['expires_at']
                    self.redirect_uri = key_dict['redirect_uri']
                    self.secret = key_dict['secret']
            if not key_exists:
                raise KeyError("Access token not found for key: " + self.key + ". Please use spr-oauth or "
                                                                               "spr-pass-auth "
                                                                               "to complete the authorization.")

    def _gen_auth(self):
        """
        Generates Auth Token from Auth Code. If successful returns response, otherwise raises Exception.
        """
        base_url = self.base_url
        if self.env != 'prod':
            base_url = base_url + self.env + "/"
        endpoint = base_url + OAUTH_PATH
        params = {
            "client_id": self.key,
            "client_secret": self.secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "code": self.auth_code
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {}
        response = requests.request(method="POST", url=endpoint, params=params, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error occurred while generating Access Token from Auth Code. Response : " + response.text)

    def _gen_pass_auth(self):
        """
        Generates Auth Token from Email and Password. If successful returns response, otherwise raises Exception.
        """

        base_url = self.base_url
        if self.env != 'prod':
            base_url = base_url + self.env + "/"
        endpoint = base_url + OAUTH_PATH
        params = {
            "client_id": self.key,
            "client_secret": self.secret,
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {}
        response = requests.request(method="POST", url=endpoint, params=params, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "Error occurred while generating Access Token from Username and Password. Response : " + response.text)

    def gen_access_token_from_refresh_token(self):
        """
        Generates Auth Token from Refresh Token. If successful returns response, otherwise raises Exception.
        """

        endpoint = self.base_url + self.env + "/" + OAUTH_PATH
        params = {
            "client_id": self.key,
            "client_secret": self.secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "refresh_token",
            "refresh_token": quote_plus(self.refresh_token)
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {}
        response = requests.request(method="POST", url=endpoint, params=params, headers=headers, data=payload)
        if response.status_code == 200:
            response = response.json()
            self.access_token, self.refresh_token = response["access_token"], response["refresh_token"]
            self.expires_at = time.time() + response["expires_in"]
            self.credentials_file.update_key(
                key=self.key, env=self.env, secret=self.secret, redirect_uri=self.redirect_uri,
                refresh_token=self.refresh_token, access_token=self.access_token, expires_at=self.expires_at)
            return response
        else:
            raise Exception(
                "Error occurred while generating Auth Token from Refresh Token. Response : " + response.text)
