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
from app import Usuario, fieldsFormatter, Perfil
from app import AuthLoginSchema
from flask_pydantic import validate
from werkzeug.security import check_password_hash

# --------------------------------------------------------------------------------------------------#


@app.route("/auth", methods=["POST"])
@validate(body=AuthLoginSchema)
def login():
    data = request.get_json()

    email = data.get("email").lower()

    cpf_pis = fieldsFormatter.CpfFormatter().clean(email)

    user = db.session.query(Usuario).join(Perfil, Perfil.id == Usuario.perfil_id, isouter=True).filter(
        or_(
            Usuario.email == email,
            Perfil.cpf == cpf_pis,
            Perfil.pis == cpf_pis
        )
    ).first()

    output = {
        "form": [],
        "error": False
    }

    if not user:
        output["form"].append({"message": Messages.AUTH_USER_NOT_FOUND})
        output["error"] = True
    elif not check_password_hash(user.senha, str(data.get("senha"))):
        output["form"].append({"message": Messages.AUTH_USER_PASS_ERROR})
        output["error"] = True

    if output["error"]:
        return jsonify(output)

    return (
        jsonify(
            {
                "access_token": create_access_token(identity=user.id),
                "refresh_token": create_refresh_token(identity=user.id),
                "cargo_id": user.cargo_id,
                "email": user.email,
                "perfil_id": user.perfil_id,
                "perfil": {
                    "id": user.perfil_id,
                    "nome": user.perfil.nome,
                    "cpf": user.perfil.cpf,
                    "pis": user.perfil.pis
                } if user.perfil_id is not None else None,
                "cargo": {
                    "id": user.cargo.id,
                    "name": user.cargo.nome
                },
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
    if user is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(current_user), "error": True})

    return (
        jsonify(
            {
                "error": False,
                "id": user.id,
                "email": user.email,
                "perfil_id": user.perfil_id,
                "perfil":{
                    "id": user.perfil_id,
                    "nome": user.perfil.nome,
                    "cpf": fieldsFormatter.CpfFormatter().format(user.perfil.cpf),
                    "pis": fieldsFormatter.PisFormatter().format(user.perfil.pis),
                    "cep": fieldsFormatter.CepFormatter().format(user.perfil.cep),
                    "rua": user.perfil.rua,
                    "numero": user.perfil.numero,
                    "complemento": user.perfil.complemento,
                    "cidade_id": user.perfil.cidade_id,
                }if user.perfil_id is not None else None,
                "cargo_id": user.cargo_id,
                "cargo": {
                    "id": user.cargo.id,
                    "name": user.cargo.nome
                },
            }
        ),
        200,
    )


# --------------------------------------------------------------------------------------------------#
