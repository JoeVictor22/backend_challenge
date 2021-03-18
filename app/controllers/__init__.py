from app import db, Messages, app
from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity

from app import Usuario
from app import Cargo
from app import Controller
from app import Regra


## OAUTH teste
import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt
from pprint import pprint
import time
# authorization
def resource(resource_name):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = Usuario.query.get(get_jwt_identity())
            user_role = user.cargo_id
            contr, act = resource_name.split("-")

            data = db.session.query(
                Regra.permitir,
                Regra.cargo_id,
                Regra.acao.label("act"),
                Controller.nome.label("contr"),
            ).join(Controller, Regra.controller_id == Controller.id).filter(
                Regra.cargo_id == user_role,
                Regra.acao == act,
                Controller.nome == contr,
            ).first()

            if data == None:
                return (
                    jsonify(
                        {
                            "description": Messages.AUTH_USER_DENIED,
                            "error": "Unauthorized Access",
                            "status_code": 401,
                        }
                    ),
                    401,
                )

            if not data.permitir:
                return (
                    jsonify(
                        {
                            "description": Messages.AUTH_USER_DENIED,
                            "error": "Unauthorized Access",
                            "status_code": 401,
                        }
                    ),
                    401,
                )

            return f(*args, **kwargs)

        return wrapped

    return wrapper

def paginate(query, page=1, rows_per_page=1):

    pagination = query.paginate(page=page, per_page=rows_per_page, error_out=False)

    data = pagination.items

    output = {
        "pagination": {
            "pages_count": pagination.pages,
            "itens_count": pagination.total,
            "itens_per_page": rows_per_page,
            "prev": pagination.prev_num,
            "next": pagination.next_num,
            "current": pagination.page,
        },
        "itens": [],
        "error": False,
    }

    return data, output


## OAuth

AUTH0_DOMAIN = 'dev-u6qbtmtr.us.auth0.com'
API_AUDIENCE = "https://web-challenge-autho"
ALGORITHMS = ["RS256"]

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token



def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")

        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        pprint(jwks)

        print(jwks["keys"][0]["kid"])
        for key in jwks["keys"]:
            print("crashou")
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

