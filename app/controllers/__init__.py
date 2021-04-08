from app import db, Messages
from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import get_jwt_identity

from app import Usuario
from app import Cargo
from app import Controller
from app import Regra

from pydantic import BaseModel, ValidationError, FilePath

from app import error_messages

# access control
def resource(resource_name):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = Usuario.query.get(get_jwt_identity())
            if user is None:
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

            if data is None:
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

# --------------------------------------------------------------------------------------------------#

# pydantic validator
def field_validator(validator):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_data()

            try:
                validator.parse_raw(data)
            except ValidationError as e:
                for error in e.errors():
                    msg = error_messages.get(error['type'])
                    ctx = error.get('ctx')

                    if msg:
                        if ctx:
                            msg = msg.format(**ctx)
                        error['msg'] = msg

                validation_errors = {
                    "body_params": e.errors()
                }

                return (
                    jsonify(
                        {
                            "validation_error": validation_errors,
                            "status_code": 400,
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)
        return wrapped
    return wrapper

# --------------------------------------------------------------------------------------------------#

# item pagination
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