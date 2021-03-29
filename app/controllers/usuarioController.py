from app import app, db, Messages
from . import resource, paginate, field_validator
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc, or_
from werkzeug.security import generate_password_hash
from app import Usuario, Perfil
from app import fieldsFormatter

from flask_pydantic import validate
from app import UsuarioAddSchema, UsuarioEditSchema
from app import CadastroAddSchema



@app.route("/usuario/all", methods=["GET"])
@jwt_required
@resource("usuario-all")
def usuarioAll():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    email_filter = request.args.get("email", None)

    query = Usuario.query

    if email_filter is not None:
        query = query.filter(Usuario.email.ilike("%%{}%%".format(email_filter.lower())))

    usuarios, output = paginate(query, page, rows_per_page)

    for usuario in usuarios:
        data = {}
        data["id"] = usuario.id
        data["email"] = usuario.email
        data["perfil_id"] = usuario.perfil_id

        data["cargo_id"] = usuario.cargo_id

        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/usuario/view/<usuario_id>", methods=["GET"])
@jwt_required
@resource("usuario-view")
def usuarioView(usuario_id):

    current_user = get_jwt_identity()
    user = Usuario.query.get(current_user)

    # guarantee that user can only view itself
    if user is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(current_user), "error": True})
    if user.cargo_id == 2:
        usuario_id = user.id

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    data = {"error": False}
    data["id"] = usuario.id
    data["email"] = usuario.email
    data["perfil_id"] = usuario.perfil_id

    data["cargo_id"] = usuario.cargo_id

    return jsonify(data)

# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/add", methods=["POST"])
@jwt_required
@resource("usuario-add")
@field_validator(UsuarioAddSchema)
def usuarioAdd():
    data = request.get_json()

    # check if perfil is already fk of a user
    if data.get("perfil_id"):
        usuario_perfil = Usuario.query.filter(Usuario.perfil_id == data["perfil_id"]).first()
        if usuario_perfil is not None:
            return jsonify(
                {"message": Messages.ALREADY_EXISTS.format("Perfil"), "error": True}
            )

    # check if is emails is already in use
    email = data.get("email").lower()
    if Usuario.query.filter_by(email=email).first():
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("email"), "error": True}
        )

    hashed_pass = generate_password_hash(data.get('senha'), method="sha256")

    usuario = Usuario(
        email=email,
        senha=hashed_pass,
        perfil_id=data.get('perfil_id'),
        cargo_id=data.get("cargo_id"),
    )

    db.session.add(usuario)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )

# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/edit/<usuario_id>", methods=["PUT"])
@jwt_required
@resource("usuario-edit")
@field_validator(UsuarioEditSchema)
def usuarioEdit(usuario_id):
    data = request.get_json()

    # get logged user
    current_user = get_jwt_identity()
    logged_user = Usuario.query.get(current_user)

    # guarantee that user can only edit itself
    if logged_user is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(current_user), "error": True})
    if logged_user.cargo_id == 2:
        usuario_id = logged_user.id

    # get user to be edited
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    # check if perfil is already fk of a user
    if data.get("perfil_id"):
        usuario_perfil = Usuario.query.filter(Usuario.perfil_id == data["perfil_id"], Usuario.id != usuario_id).first()
        if usuario_perfil is not None:
            return jsonify(
                {"message": Messages.ALREADY_EXISTS.format("Perfil"), "error": True}
            )

    # check if is emails is already in use
    email = data.get("email").lower()
    if Usuario.query.filter(Usuario.email == email, Usuario.id != usuario_id).first():
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("email"), "error": True}
        )

    # if user is trying to edit itself, let it change password
    if logged_user.id == usuario.id:
        # check should change password
        if data.get('senha') is not None:
            hashed_pass = generate_password_hash(data.get('senha'), method="sha256")
            usuario.senha = hashed_pass

    usuario.email = email
    usuario.perfil_id = data.get("perfil_id")
    usuario.cargo_id = data.get("cargo_id")

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_UPDATED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )

# --------------------------------------------------------------------------------------------------#


@app.route("/usuario/delete/<usuario_id>", methods=["DELETE"])
@jwt_required
@resource("usuario-delete")
def usuarioDelete(usuario_id):

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    current_user = get_jwt_identity()
    usuario_logado = Usuario.query.get(current_user)

    if usuario_logado.cargo_id != 1 and usuario_logado.id != usuario.id:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})


    db.session.delete(usuario)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_DELETED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Messages.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/cadastro", methods=["POST"])
@field_validator(CadastroAddSchema)
def cadastroAdd():
    data = request.get_json()

    # if there is already a user with email

    if Usuario.query.filter_by(email=data.get("email").lower()).first():
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
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#
