from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from sqlalchemy import or_
from app import Usuario, fieldsFormatter, Pessoa
from app import AuthValidator, AuthLoginSchema
from flask_pydantic import validate
from werkzeug.security import check_password_hash

# --------------------------------------------------------------------------------------------------#


@app.route("/auth", methods=["POST"])
@validate(body=AuthLoginSchema)
def login():
    data = request.get_json()

    cpf_pis = fieldsFormatter.CpfFormatter().clean(data.get("email"))


    user = db.session.query(Usuario).join(Pessoa, Pessoa.id == Usuario.pessoa_id, isouter=True).filter(
        or_(
            Usuario.email == data.get("email"),
            Pessoa.cpf == cpf_pis,
            Pessoa.pis == cpf_pis
        )
    ).first()


    error = {
        "form": [],
        "has": False
    }

    if not user:
        error["form"].append({"message": Messages.AUTH_USER_NOT_FOUND})
        error["has"] = True
    elif not check_password_hash(user.senha, str(data.get("senha"))):
        error["form"].append({"message": Messages.AUTH_USER_PASS_ERROR})
        error["has"] = True

    if error["has"]:
        return jsonify(error)

    return (
        jsonify(
            {
                "access_token": create_access_token(identity=user.id),
                "refresh_token": create_refresh_token(identity=user.id),
                "cargo_id": user.cargo_id,
            }
        ),
        200,
    )


# --------------------------------------------------------------------------------------------------#


@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    return jsonify({"access_token": create_access_token(identity=current_user)}), 200


# --------------------------------------------------------------------------------------------------#


@app.route("/me", methods=["GET"])
@jwt_required
def me():
    current_user = get_jwt_identity()
    user = Usuario.query.get(current_user)
    return (
        jsonify(
            {
                "email": user.email,
                "pessoa_id": user.pessoa_id,
                "pessoa":{
                    "id": user.cargo_id,
                    "nome": user.pessoa.nome,
                    "cpf": user.pessoa.cpf,
                    "pis": user.pessoa.pis
                },
                "cargo_id": user.cargo_id,
                "cargo": {
                    "id": user.cargo.id,
                    "name": user.cargo.name
                },
            }
        ),
        200,
    )


# --------------------------------------------------------------------------------------------------#
