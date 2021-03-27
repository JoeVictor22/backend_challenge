from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc, or_
from werkzeug.security import generate_password_hash
from app import Usuario, Perfil
from app import fieldsFormatter

from flask_pydantic import validate
from app import CadastroAddSchema
from traceback import print_exc

# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/cadastro", methods=["POST"])
@validate(body=CadastroAddSchema)
def cadastroAdd():
    data = request.get_json()

    # if there is already a user with email
    if Usuario.query.filter_by(email=data.get["email"]).first():
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("email"), "error": True}
        )

    # check if there is already a user with cpf/pis
    cpf = fieldsFormatter.CpfFormatter().clean(data["cpf"])
    pis = fieldsFormatter.PisFormatter().clean(data["pis"])
    perfil = Perfil.query.filter(or_(Perfil.cpf == cpf, Perfil.pis == pis)).first()
    if perfil is not None:
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

    hashed_pass = generate_password_hash(data.get('senha'), method="sha256")
    email = data.get("email").lower()

    perfil = Perfil(
        nome=data.get("nome"),
        pis=fieldsFormatter.PisFormatter().clean(data.get("pis")),
        cpf=fieldsFormatter.CpfFormatter().clean(data.get("cpf")),
        cep=fieldsFormatter.CepFormatter().clean(data.get("cep")),
        rua=data.get("rua"),
        numero=data.get("numero"),
        complemento=data.get("complemento"),
        cidade_id=data.get("cidade_id"),
    )

    db.session.add(perfil)

    try:
        db.session.flush()

        usuario = Usuario(
            email=email,
            senha=hashed_pass,
            perfil_id=perfil.id,
            cargo_id=2,
        )

        db.session.add(usuario)

        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        print_exc()
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#
