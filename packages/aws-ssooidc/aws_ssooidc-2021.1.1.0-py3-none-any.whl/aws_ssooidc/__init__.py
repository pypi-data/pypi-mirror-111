#!/usr/bin/env python3
"""Execute AWS SSO auth tasks."""
import boto3
import json
import os.path
import glob
import webbrowser
import time


__version__ = '2021.1.1.0'


class FailedToGetFileException(Exception):
    """Raised when the JSON cache fails file check."""

    pass


def createclient(
    client_name: str,
    client_type: str = 'public',
    region: str = 'us-east-1'
) -> dict:
    """
    Create SSO client for authorization.

    return dict
    """
    # Create client.
    sso_oidc = boto3.client(
        'sso-oidc',
        region_name=region
    )

    # Register client.
    response = sso_oidc.register_client(
        clientName=client_name,
        clientType=client_type
        # scopes=[
        #     'string',
        # ]
    )

    return response


def startauth(
    client_id: str,
    client_secret: str,
    start_url: str,
    region: str = 'us-east-1'
) -> dict:
    """
    Start SSO authorization process.

    return dict
    """
    # Create client.
    sso_oidc = boto3.client(
        'sso-oidc',
        region_name=region
    )

    # Start authentication process.
    response = sso_oidc.start_device_authorization(
        clientId=client_id,
        clientSecret=client_secret,
        startUrl=start_url
    )

    return response


def getclienttoken(
    client_id: str,
    client_secret: str,
    device_code: str,
    grant_type: str = 'urn:ietf:params:oauth:grant-type:device_code',
    region: str = 'us-east-1'
) -> dict:
    """
    Get SSO Access Token from client authorization (recommended).

    Supports grant types for authorization code,
    refresh token, and device code requests.

    return dict
    """
    # Create client.
    sso_oidc = boto3.client(
        'sso-oidc',
        region_name=region
    )

    # Get tokens.
    response = sso_oidc.create_token(
        clientId=client_id,
        clientSecret=client_secret,
        grantType=grant_type,
        deviceCode=device_code
    )

    return response


def getjsontoken(
    json_cache: str = None
) -> dict:
    """
    Get SSO Access Token from SSO JSON cache.

    If an SSO JSON cache file is specified, use it. Otherwise, use the
    newest ".json" file in "~/.aws/sso/cache/".

    Login to SSO using AWSCLI if token doesn't exist or has expired.
    Command: aws sso login [--profile <your-SSO-profile-if-not-default>]

    return dict
    """
    # Expand home directory if specified witha tilde.
    home = os.path.expanduser("~")

    # Get JSON cache file from argument or from default location.
    try:
        assert json_cache is not None
        if json_cache.startswith('~'):
            json_cache = json_cache.replace('~', home)
    except Exception as e:
        list_of_files = glob.glob('{}/.aws/sso/cache/*.json'.format(home))
        json_cache = max(list_of_files, key=os.path.getctime)

    # Raise exception if specified JSON cache file
    # is not a file or does not exist.
    if not os.path.isfile(json_cache):
        raise FailedToGetFileException('Failed to get JSON cache file')

    # Get Access Token and expiry from JSON cache.
    with open(json_cache, 'r') as f:
        response = json.load(f)

    return response


def gettoken(
    start_url: str,
    client_name: str = 'ssoclient',
    region: str = 'us-east-1',
    timeout=30
) -> dict:
    """
    Get SSO Access Token using getclienttoken.

    Run the full process:
    1. createclient
    2. startauth
    3. getclienttoken

    return dict
    """
    # Create authorization client.
    response_create = createclient(
        client_name,
        region=region
    )

    # Start client authorization process.
    response_start = startauth(
        response_create['clientId'],
        response_create['clientSecret'],
        start_url,
        region=region
    )

    print(
        'Verification URI: {}'.
        format(response_start['verificationUriComplete'])
    )

    # Open web browser for authentication.
    response_web = webbrowser.open(
        response_start['verificationUriComplete'],
        new=2,
        autoraise=True
    )

    # Try and retry to get Access Token
    # while browser authentication is running.
    # Fail after 10 tries.
    get_counter = 0
    while True:
        try:
            assert get_counter <= timeout
            response = getclienttoken(
                response_create['clientId'],
                response_create['clientSecret'],
                response_start['deviceCode'],
                region=region
            )
            break
        except Exception as e:
            time.sleep(1)
            get_counter += 1
            if get_counter > timeout:
                break
            pass

    try:
        response
        return response
    except Exception as e:
        return {
            'message': (
                'Failed to get Access Token after {} tries.'
                .format(timeout)
            )
        }
