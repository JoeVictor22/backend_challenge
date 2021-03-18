from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from . import resource, paginate
from app import Usuario, Pessoa
from app import fieldsFormatter

from pprint import pprint
from flask_pydantic import validate
from app import CadastroAddSchema
from traceback import print_exc

# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/cadastro", methods=["POST"])
@validate(body=CadastroAddSchema)
def cadastroAdd():
    data = request.get_json()

    hashed_pass = generate_password_hash(data.get('senha'), method="sha256")
    email = data.get("email").lower()

    pessoa = Pessoa(
        nome=data.get("nome"),
        pis=fieldsFormatter.PisFormatter().clean(data.get("pis")),
        cpf=fieldsFormatter.CpfFormatter().clean(data.get("cpf")),
        cep=fieldsFormatter.CepFormatter().clean(data.get("cep")),
        rua=data.get("rua"),
        numero=data.get("numero"),
        complemento=data.get("complemento"),
        cidade_id=data.get("cidade_id"),
    )

    db.session.add(pessoa)

    try:
        db.session.flush()

        usuario = Usuario(
            email=email,
            senha=hashed_pass,
            pessoa_id=pessoa.id,
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
