from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from . import resource, paginate
from app import Perfil
from app import UsuarioValidator
from app import fieldsFormatter

from pprint import pprint
from flask_pydantic import validate
from app import PerfilAddSchema


@app.route("/perfil/all", methods=["GET"])
@jwt_required
@resource("perfil-all")
def perfilAll():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)

    query = Perfil.query

    perfis, output = paginate(query, page, rows_per_page)

    for perfil in perfis:
        data = {}
        data["id"] = perfil.id
        data["nome"] = perfil.nome
        data["pis"] = fieldsFormatter.PisFormatter().format(perfil.pis)
        data["cpf"] = fieldsFormatter.CpfFormatter().format(perfil.cpf)
        data["cep"] = fieldsFormatter.CepFormatter().format(perfil.cep)
        data["rua"] = perfil.rua
        data["numero"] = perfil.numero
        data["complemento"] = perfil.complemento
        data["cidade_id"] = perfil.cidade_id


        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/perfil/view/<perfil_id>", methods=["GET"])
@jwt_required
@resource("perfil-view")
def perfilView(perfil_id):
    perfil = Perfil.query.get(perfil_id)

    if not perfil:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(perfil_id), "error": True}
        )

    data = {"error": False}
    data["id"] = perfil.id
    data["nome"] = perfil.nome
    data["pis"] = fieldsFormatter.PisFormatter().format(perfil.pis)
    data["cpf"] = fieldsFormatter.CpfFormatter().format(perfil.cpf)
    data["cep"] = fieldsFormatter.CepFormatter().format(perfil.cep)
    data["rua"] = perfil.rua
    data["numero"] = perfil.numero
    data["complemento"] = perfil.complemento
    data["cidade_id"] = perfil.cidade_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route("/perfil/add", methods=["POST"])
@jwt_required
@resource("perfil-add")
@validate(body=PerfilAddSchema)
def perfilAdd():
    data = request.get_json()


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
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Perfil"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/perfil/edit/<perfil_id>", methods=["PUT"])
@jwt_required
@resource("perfil-edit")
@validate(body=PerfilAddSchema)
def perfilEdit(perfil_id):
    perfil = Perfil.query.get(perfil_id)

    if not perfil:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(perfil_id), "error": True}
        )

    data = request.get_json()

    perfil.nome = data.get("nome")
    perfil.pis = fieldsFormatter.PisFormatter().clean(data.get("pis")),
    perfil.cpf = fieldsFormatter.CpfFormatter().clean(data.get("cpf")),
    perfil.cep = fieldsFormatter.CepFormatter().clean(data.get("cep"))
    perfil.rua = data.get("rua")
    perfil.numero = data.get("numero")
    perfil.complemento = data.get("complemento")
    perfil.cidade_id = data.get("cidade_id")

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_UPDATED.format("Perfil"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/perfil/delete/<perfil_id>", methods=["DELETE"])
@jwt_required
@resource("perfil-delete")
def perfilDelete(perfil_id):
    perfil = Perfil.query.get(perfil_id)

    if not perfil:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(perfil_id), "error": True}
        )

    db.session.delete(perfil)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_DELETED.format("Perfil"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Messages.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )
