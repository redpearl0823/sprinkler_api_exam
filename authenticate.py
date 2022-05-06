from getpass import getpass
import logging
from pathlib import Path

from . import credentials
from .spr_auth import SprAuth
from spr_api.spr_auth import DEFAULT_BASE_URL

import argparse


def password_auth():
    parser = createArgumentParser()
    parser.add_argument(
        "--store",
        "-s",
        type=Path,
        metavar="PATH",
        default=credentials.DEFAULT_CREDENTIALS_PATH,
        help="Path to where access tokens are stored."
    )
    parser.add_argument(
        "--environment",
        "-env",
        type=str,
        default="prod",
        help="Sprinklr Environment."
    )
    parser.add_argument(
        "--client_id",
        "-cId",
        type=str,
        help="Your Mashery Application Client Id."
    )
    parser.add_argument(
        "--client_secret",
        "-cS",
        type=str,
        help="Your Mashery Application Client Secret."
    )
    parser.add_argument(
        "--redirect_url",
        "-rL",
        type=str,
        help="Your Mashery Application Redirect Link."
    )
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="Your Sprinklr email address."
    )
    parser.add_argument(
        "--password",
        "-p",
        type=str,
        help="Your Sprinklr Password."
    )

    args = parser.parse_args()

    if args.environment is None or args.client_id is None or args.client_secret is None or args.username is None or args.password is None:
        print("Please enter your Sprinklr credentials below")
        if args.client_id is None:
            args.client_id = input("Mashery Application Id: ")
            ensure_not_none_value(args.client_id)
        if args.client_secret is None:
            args.client_secret = input("Mashery Application Secret: ")
            ensure_not_none_value(args.client_id)
        if args.redirect_url is None:
            args.redirect_url = input("Mashery Application Redirect Link: ")
            ensure_not_none_value(args.client_id)
        if args.username is None:
            args.username = input("Email: ")
            ensure_not_none_value(args.username)
        if args.password is None:
            args.password = getpass("Password: ")
            ensure_not_none_value(args.password)

    try:
        print("Authenticating user to {} : {}".format(args.environment, args.username))
        SprAuth(env=args.environment, key=args.client_id, secret=args.client_secret, redirect_uri=args.redirect_url,
                username=args.username, password=args.password)
        print("Success!")
    except KeyError as e:
        print(e)


def oauth():
    parser = createArgumentParser()

    parser.add_argument(
        "--store",
        "-s",
        type=Path,
        metavar="PATH",
        default=credentials.DEFAULT_CREDENTIALS_PATH,
        help="Path to where access tokens are stored."
    )
    parser.add_argument(
        "--environment",
        "-env",
        type=str,
        default="prod",
        help="Sprinklr Environment."
    )
    parser.add_argument(
        "--client_id",
        "-cId",
        type=str,
        help="Your Mashery Application Client Id."
    )
    parser.add_argument(
        "--client_secret",
        "-cS",
        type=str,
        help="Your Mashery Application Client Secret."
    )
    parser.add_argument(
        "--redirect_url",
        "-rL",
        type=str,
        help="Your Mashery Application Redirect Link."
    )
    parser.add_argument(
        "--authorization_code",
        "-c",
        type=str,
        help="Authorization Code."
    )

    args = parser.parse_args()

    if args.environment is None or args.client_id is None or args.client_secret is None or args.username is None or args.password is None:
        print("Please enter your Sprinklr credentials below")
        if args.client_id is None:
            args.client_id = input("Mashery Application Id: ")
            ensure_not_none_value(args.client_id)
        if args.client_secret is None:
            args.client_secret = input("Mashery Application Secret: ")
            ensure_not_none_value(args.client_secret)
        if args.redirect_url is None:
            args.redirect_url = input("Mashery Application Redirect Link: ")
            ensure_not_none_value(args.redirect_url)

    try:
        url = DEFAULT_BASE_URL
        if args.environment != 'prod':
            url = url + args.environment + "/"
        print("Please click or copy paste the link in your browser to authorize access to your sprinklr {} environment."
              " {}oauth/authorize?client_id={}&response_type=code&redirect_uri={}"
              .format(args.environment, url, args.client_id, args.redirect_url))
        args.code = input("Please enter the authorization code returned to your redirect url: ")
        ensure_not_none_value(args.code)
        print("Authenticating user to {}".format(args.environment))
        SprAuth(env=args.environment, key=args.client_id, secret=args.client_secret, redirect_uri=args.redirect_url,
                auth_code=args.code)
        print("Success!")
    except KeyError as e:
        print(e)


def ensure_not_none_value(value):
    if value is None:
        raise RuntimeError("Please fill in all mandatory parameters")


def createArgumentParser():
    logger = logging.getLogger("spr_api")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    parser = argparse.ArgumentParser(
        description="Logging to Sprinklr and retrieve and access token and refresh token.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    return parser


if __name__ == "__password_auth__":
    password_auth()

if __name__ == "__oauth__":
    oauth()
