from pathlib import Path
import pickle
import os

import sys

DEFAULT_CREDENTIALS_PATH = Path(os.path.expanduser("~")) / ".sprinklr" / "auth_file.txt"

"""
Credentials file stores details about different envs and keys in below format as a dictionary
{
    env1 : {
        key1: {"secret": secret1, "redirect_uri": redirect_uri1, "access_token": access_token1 , "expires_at": expires_at1, "refresh_token": refresh_token1 },
        key2: {"secret": secret2, "redirect_uri": redirect_uri2, "access_token": access_token2 , "expires_at": expires_at2, "refresh_token": refresh_token2 },
        .....
    },
    env2 : {
        key3: {"secret": secret3, "redirect_uri": redirect_uri3, "access_token": access_token3, "expires_at": expires_at3, "refresh_token": refresh_token3 },
        key4: {"secret": secret4, "redirect_uri": redirect_uri4, "access_token": access_token4 , "expires_at": expires_at4, "refresh_token": refresh_token4 },
        ....
    },
    ....
}

expires_at is in seconds (from epoch)
"""


class CredentialsFile:
    def __init__(self, credentials_file_path=None):
        credentials_file_path = credentials_file_path if credentials_file_path is not None else DEFAULT_CREDENTIALS_PATH
        self.credentials_file = Path(credentials_file_path)
        directory = os.path.dirname(credentials_file_path)
        if not os.path.exists(directory):
            Path(directory).mkdir(parents=True, exist_ok=True)
        self.credentials_file.touch(exist_ok=True)

    def read_file(self):
        with open(self.credentials_file, 'rb') as f:
            try:
                self.credentials_file_dict = pickle.load(f)
            except EOFError:
                self.credentials_file_dict = {}
            return self.credentials_file_dict

    def update_key(self, key, env, secret, redirect_uri, access_token, refresh_token, expires_at):

        if (secret is None) or (redirect_uri is None) or (access_token is None) or (refresh_token is None) or (
                expires_at is None):
            raise ValueError("Error save new auth token, not all parameters are being generated correctly.")

        with open(self.credentials_file, 'rb') as f:
            try:
                env_dict = pickle.load(f)
            except EOFError:
                env_dict = {}

        if env not in env_dict:
            env_dict[env] = {}
        if key not in env_dict[env]:
            env_dict[env][key] = {}

        if secret is not None:
            env_dict[env][key]["secret"] = secret
        if redirect_uri is not None:
            env_dict[env][key]["redirect_uri"] = redirect_uri
        if access_token is not None:
            env_dict[env][key]["access_token"] = access_token
        if refresh_token is not None:
            env_dict[env][key]["refresh_token"] = refresh_token
        if expires_at is not None:
            env_dict[env][key]["expires_at"] = expires_at

        with open(self.credentials_file, 'wb') as f:
            pickle.dump(env_dict, f)
