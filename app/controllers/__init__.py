from app import db, Messages
from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity

from app import Usuario
from app import Cargo
from app import Controller
from app import Regra

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

            if not data.allow:
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