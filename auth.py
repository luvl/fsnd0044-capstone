import json

from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from exceptions import AUTH_ERROR
from config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE


## Auth Header
# https://dev-6rl2das1i31tydyi.us.auth0.com/authorize?audience=casting_agency_api&response_type=token&client_id=pegk0biZtugIfRpr1RWO9nlPsn70TF3R&redirect_uri=https://127.0.0.1:8080/login-results
'''
    get_token_auth_header() method
        it should attempt to get the header from the request
            it should raise an AUTH_ERROR if no header is present
        it should attempt to split bearer and the token
            it should raise an AUTH_ERROR if the header is malformed
        return the token part of the header
'''


# reference: https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AUTH_ERROR({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AUTH_ERROR({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AUTH_ERROR({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AUTH_ERROR({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
    check_permissions(permission, payload) method
        it should raise an AUTH_ERROR if permissions are not included in the payload
        it should raise an AUTH_ERROR if the requested permission string is not in the payload permissions array
        return true otherwise
'''


# reference: https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AUTH_ERROR({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AUTH_ERROR({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


'''
    verify_decode_jwt(token) method
        it should be an Auth0 token with key id (kid)
        it should verify the token using Auth0 /.well-known/jwks.json
        it should decode the payload from the token
        it should validate the claims
        return the decoded payload
'''


# reference: https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AUTH_ERROR({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AUTH_ERROR({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AUTH_ERROR({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AUTH_ERROR({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AUTH_ERROR({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
    @requires_auth(permission) decorator method
        it should use the get_token_auth_header method to get the token
        it should use the verify_decode_jwt method to decode the jwt
        it should use the check_permissions method validate claims and check the requested permission
        return the decorator which passes the decoded payload to the decorated method
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