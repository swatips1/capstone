import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
CALLBACK_URLS = os.environ.get('CALLBACK_URLS')
LOGOUT_URLS = os.environ.get('LOGOUT_URLS')
WEBORIGIN_URLS = os.environ.get('WEBORIGIN_URLS')
CORS_URLS = os.environ.get('CORS_URLS')
ID_TOKEN_EXPIRATION = os.environ.get('ID_TOKEN_EXPIRATION')
TOKEN_EXPIRATION = os.environ.get('TOKEN_EXPIRATION')
TOKEN_EXPIRATION_BROWSER = os.environ.get('TOKEN_EXPIRATION_BROWSER')
ENABLE_RBAC = os.environ.get('ENABLE_RBAC')
ADD_PERMISSIONS_TO_TOKEN = os.environ.get('ADD_PERMISSIONS_TO_TOKEN')


# Login URL:
# https://spskelly.us.auth0.com/authorize?audience=choremonsta&response_type=token&client_id=PBFYXnZc3cLsQ5WNJvYmxbV7ObZIh4xc&redirect_uri=http://localhost:8100/


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
get_token_auth_header() method.
Attempts to get the header from the request.
Raises an AuthError if no header is present.
Otherwise, attempts to split bearer and the token.
Raises an AuthError if the header is malformed.
When successful, returns the token part of the header
'''


def get_token_auth_header():
    # attempt to get the header from the request
    auth_headers = request.headers.get('Authorization', None)
    if not auth_headers:
        raise AuthError({
            'code': 'no_auth_in_header',
            'description': 'No authorization details in request header.'
        }, 401)
    header_parts = auth_headers.split()

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'no_bearer_tag',
            'description': 'Bearer tag not present or malformed.'
        }, 401)

    elif len(header_parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'too_many_parts',
            'description': 'Too many parts to Auth header.'
        }, 401)

    token = header_parts[1]
    return token


'''
check_permissions(permission, payload)
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    Raises an AuthError if permissions are not included in the payload
    Raises an AuthError if the requested permission string is not
    in the payload permissions array. Returns true otherwise
'''


def check_permissions(permission, payload):
    # raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload:
        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)
    # raise an AuthError if the requested permission string is
    # not in the payload permissions array
    if permission not in payload['permissions']:
        # print('cant find', permission)
        raise AuthError({
                        'code': 'unauthorized',
                        'description': 'Permission not in payload.'
                        }, 401)
    return True


'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    Verifies the token using Auth0 /.well-known/jwks.json
    Decodes the payload from the token
    Validates the claims
    returns the decoded payload
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Get Header
    unverified_header = jwt.get_unverified_header(token)
    # Whats the key?
    rsa_key = {}
    # check it is an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
                            'code': 'invalid_header',
                            'description': 'Authorization malformed.'
                        }, 401)
    for key in jwks['keys']:
        # verify the token using Auth0 /.well-known/jwks.json
        if key['kid'] == unverified_header['kid']:
            # decode the payload from the token
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # What do we have here?
    if rsa_key:
        # validate the claims
        try:
            # Decode the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # return the decoded payload
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                                'code': 'token_expired',
                                'description': 'Token is expired.'
                            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check audience & issuer.'
                }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError({
                        'code': 'invalid_header',
                        'description': 'Unable to find the appropriate key.'
                    }, 400)


'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    Uses the get_token_auth_header method to get the token
    Calls the verify_decode_jwt method to decode the jwt
    Calls the check_permissions method validate claims
    and check the requested permission
    returns the decorator which passes the decoded
    payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
