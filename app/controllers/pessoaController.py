from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from . import resource, paginate
from app import Pessoa
from app import UsuarioValidator
from app import fieldsFormatter

from pprint import pprint
from flask_pydantic import validate
from app import PessoaAddSchema


@app.route("/pessoa/all", methods=["GET"])
@jwt_required
@resource("pessoa-all")
def pessoaAll():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)

    query = Pessoa.query

    pessoas, output = paginate(query, page, rows_per_page)

    for pessoa in pessoas:
        data = {}
        data["id"] = pessoa.id

        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/pessoa/view/<pessoa_id>", methods=["GET"])
@jwt_required
@resource("pessoa-view")
def pessoaView(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(pessoa_id), "error": True}
        )

    data = {"error": False}
    data["id"] = pessoa.id


    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route("/pessoa/add", methods=["POST"])
@jwt_required
@resource("pessoa-add")
@validate(body=PessoaAddSchema)
def pessoaAdd():
    data = request.get_json()


    pessoa = Pessoa(
        email=data.get("email"),
        pessoa_id=data.get('pessoa_id'),
        cargo_id=data.get("cargo_id"),
    )

    db.session.add(pessoa)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Pessoa"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/pessoa/edit/<pessoa_id>", methods=["PUT"])
@jwt_required
@resource("pessoa-edit")
def pessoaEdit(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(pessoa_id), "error": True}
        )

    data = request.get_json()

    pessoa.email = data.get("email")
    pessoa.pessoa_id = data.get("pessoa_id")
    pessoa.cargo_id = data.get("cargo_id")

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_UPDATED.format("Pessoa"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/pessoa/delete/<pessoa_id>", methods=["DELETE"])
@jwt_required
@resource("pessoa-delete")
def pessoaDelete(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(pessoa_id), "error": True}
        )


    db.session.delete(pessoa)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_DELETED.format("Pessoa"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Messages.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )
