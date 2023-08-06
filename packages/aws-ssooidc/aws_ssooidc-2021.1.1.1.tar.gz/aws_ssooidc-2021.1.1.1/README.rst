===============
**aws_ssooidc**
===============

Overview
--------

Create temporary credentials for AWS SSO-OIDC.

Prerequisites
-------------

- *Python >= 3.6*
- *boto3 >= 1.17.78* (installed as a dependency)

Required (Positional) Arguments
-------------------------------

- Position 1: start_url (the start URL for your AWS SSO login)

Optional (Keyword) Arguments
----------------------------

- client_name
    - Description: Arbitrary name of the SSO client to create.
    - Type: String
    - Default: 'ssoclient'
- region
    - Description: Your AWS region.
    - Type: String
    - Default: 'us-east-1'
- timeout
    - Description: Number of tries before giving up.
    - Type: Integer
    - Default: 30

Usage
-----

Installation:

.. code-block:: BASH

   pip3 install aws-ssooidc
   # or
   python3 -m pip install aws-ssooidc

In Python3:

.. code-block:: BASH

   import aws_ssooidc as sso
   response = sso.gettoken('<start_url>')

   # To get Access Token:
   access_token = response['accessToken']

In BASH:

.. code-block:: BASH

   python3 -c "
       import aws_ssooidc as sso
       response = sso.gettoken('<start_url>')

       # To get Access Token:
       access_token = response['accessToken']
   "
