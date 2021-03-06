from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc, or_
from . import resource, paginate, field_validator
from app import Perfil, Usuario
from app import fieldsFormatter

from flask_pydantic import validate
from app import PerfilAddSchema


@app.route("/perfil/all", methods=["GET"])
@jwt_required
@resource("perfil-all")
def perfilAll():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    cpf = request.args.get("cpf", None)

    query = Perfil.query

    if cpf != None:
        query = query.filter(Perfil.cpf.ilike("%%{}%%".format(fieldsFormatter.CpfFormatter().clean(cpf))))

    perfis, output = paginate(query, page, rows_per_page)

    for perfil in perfis:
        data = perfil.to_dict()
        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/perfil/view/<int:perfil_id>", methods=["GET"])
@jwt_required
@resource("perfil-view")
def perfilView(perfil_id: int):

    current_user = get_jwt_identity()
    user = Usuario.query.get(current_user)

    if user is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(current_user), "error": True})

    # guarantee that user can only view itself
    if user.cargo_id == 2:
        perfil_id = user.perfil_id

    perfil = Perfil.query.get(perfil_id)

    if not perfil:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(perfil_id), "error": True}
        )

    data = perfil.to_dict()
    data['error'] = False

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route("/perfil/add", methods=["POST"])
@jwt_required
@resource("perfil-add")
@field_validator(PerfilAddSchema)
def perfilAdd():

    data = request.get_json()

    # check if there is already a user registered
    cpf = fieldsFormatter.CpfFormatter().clean(data["cpf"])
    pis = fieldsFormatter.PisFormatter().clean(data["pis"])
    perfil = Perfil.query.filter(or_(Perfil.cpf == cpf, Perfil.pis == pis)).first()
    if perfil is not None:
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

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


@app.route("/perfil/edit/<int:perfil_id>", methods=["PUT"])
@jwt_required
@resource("perfil-edit")
@field_validator(PerfilAddSchema)
def perfilEdit(perfil_id: int):
    data = request.get_json()

    current_user = get_jwt_identity()
    user = Usuario.query.get(current_user)

    # guarantee that user can only view itself
    if user is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(current_user), "error": True})
    if user.cargo_id == 2:
        perfil_id = user.perfil_id

    # check if there is already a user registered, excluding itself
    cpf = fieldsFormatter.CpfFormatter().clean(data["cpf"])
    pis = fieldsFormatter.PisFormatter().clean(data["pis"])
    perfil = Perfil.query.filter(or_(Perfil.cpf == cpf, Perfil.pis == pis)).filter(Perfil.id != perfil_id).first()
    if perfil is not None:
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )


    perfil = Perfil.query.get(perfil_id)

    if not perfil:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(perfil_id), "error": True}
        )

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


@app.route("/perfil/delete/<int:perfil_id>", methods=["DELETE"])
@jwt_required
@resource("perfil-delete")
def perfilDelete(perfil_id: int):
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
