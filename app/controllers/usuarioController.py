from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from . import resource, paginate
from app import Usuario
from app import UsuarioValidator
from app import fieldsFormatter


from pprint import pprint
from flask_pydantic import validate
from app import UsuarioAddSchema, UsuarioEditSchema

@app.route("/usuario/all", methods=["GET"])
@jwt_required
@resource("usuario-all")
def usuarioAll():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    email_filter = request.args.get("email_filter", None)

    query = Usuario.query

    if email_filter != None:
        query = query.filter(Usuario.email.ilike("%%{}%%".format(email_filter)))

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
@validate(body=UsuarioAddSchema)
def usuarioAdd():

    data = request.get_json()

    hashed_pass = generate_password_hash(data.get('senha'), method="sha256")
    email = data.get("email").lower()

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
@validate(body=UsuarioEditSchema)
def usuarioEdit(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    data = request.get_json()

    usuario.email = data.get("email").lower()
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
    
    # VALIDATE DELETE
    if usuario.id == usuario_logado.id:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})
    if usuario_logado.cargo_id != 1:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})
    if usuario.id == 1:
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
